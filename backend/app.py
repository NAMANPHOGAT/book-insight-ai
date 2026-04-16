from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# In-memory storage
books = []

# AI model
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_or_create_collection(name="books")

# 📚 Scrape Books
@app.route('/scrape', methods=['POST'])
def scrape():
    global books
    books = []

    url = "https://books.toscrape.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for i, b in enumerate(soup.select(".product_pod")[:10]):
        title = b.h3.a["title"]

        book = {
            "id": str(i),
            "title": title,
            "description": "This is a good book"
        }
        books.append(book)

        embedding = model.encode(book["description"]).tolist()

        collection.add(
            documents=[book["description"]],
            embeddings=[embedding],
            ids=[book["id"]]
        )

    return jsonify({"message": "Books scraped"})

# 📖 Get Books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# 🤖 Ask Question (RAG)
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")

    q_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=2
    )

    return jsonify({
        "question": question,
        "answer": results['documents'][0]
    })

if __name__ == '__main__':
    app.run(debug=True)