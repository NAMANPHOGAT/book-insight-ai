from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import chromadb
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# In-memory storage
books = []

# AI model
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_or_create_collection(name="books")

@app.route('/scrape', methods=['POST'])
def scrape():
    global books, collection
    books = []

    # ✅ FIX: Reset collection properly
    try:
        client.delete_collection(name="books")
    except:
        pass  # ignore if not exists

    collection = client.get_or_create_collection(name="books")

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

    return jsonify({"message": "Books scraped successfully"})


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/scrape', methods=['POST'])
def scrape():
    global books
    books = []
    collection.delete(where={})  # clear old data

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


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

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
