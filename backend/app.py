from flask import Flask, request, jsonify, send_from_directory
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__, static_folder="../frontend", static_url_path="")

books = []

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()
collection = client.get_or_create_collection(name="books")


@app.route('/')
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/scrape', methods=['POST'])
def scrape():
    global books, collection
    books = []

    try:
        client.delete_collection(name="books")
    except:
        pass

    collection = client.get_or_create_collection(name="books")

    data = [
        {
            "title": "Atomic Habits",
            "description": "A practical guide to building good habits and breaking bad ones through small daily improvements.",
            "genre": "Self-Improvement"
        },
        {
            "title": "The Alchemist",
            "description": "A philosophical story about a young shepherd pursuing his dreams and discovering his true purpose.",
            "genre": "Fiction / Philosophy"
        },
        {
            "title": "Rich Dad Poor Dad",
            "description": "A book that teaches financial literacy and the importance of assets, investments, and mindset.",
            "genre": "Finance"
        },
        {
            "title": "Ikigai",
            "description": "Explores the Japanese concept of finding purpose and living a meaningful and balanced life.",
            "genre": "Self-Help"
        },
        {
            "title": "Deep Work",
            "description": "Focuses on the ability to concentrate without distraction and produce high-quality work.",
            "genre": "Productivity"
        },
        {
            "title": "Think and Grow Rich",
            "description": "A classic book on success principles, emphasizing mindset, belief, and persistence.",
            "genre": "Motivation"
        }
    ]

    for i, b in enumerate(data):
        summary = "Summary: " + b["description"][:120] + "..."

        book = {
            "id": str(i),
            "title": b["title"],
            "description": b["description"],
            "summary": summary,
            "genre": b["genre"]
        }

        books.append(book)

        embedding = model.encode(b["description"]).tolist()

        collection.add(
            documents=[b["description"]],
            embeddings=[embedding],
            ids=[book["id"]]
        )

    return jsonify({"message": "Books loaded successfully"})


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")

    q_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=3
    )

    context = results['documents'][0]

    answer = (
        "Based on relevant books:\n\n" +
        "\n\n".join(context) +
        "\n\nThese books share similar ideas related to your query."
    )

    return jsonify({"answer": answer})


@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.json.get("title")

    selected = next((b for b in books if b["title"] == title), None)

    if not selected:
        return jsonify({"error": "Book not found"}), 404

    embedding = model.encode(selected["description"]).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=4
    )

    recommended_ids = results['ids'][0]

    recommendations = []

    for b in books:
        if b["id"] in recommended_ids and b["title"] != title:
            explanation = (
                f"If you like {title}, you may also like {b['title']} "
                f"because both focus on {selected['genre'].lower()} themes "
                f"and share similar ideas about {selected['description'][:60]}..."
            )

            recommendations.append({
                "title": b["title"],
                "genre": b["genre"],
                "explanation": explanation
            })

    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)