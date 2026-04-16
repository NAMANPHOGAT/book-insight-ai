# AI-Powered Book Insight Platform

## Overview

This project is a full-stack AI-powered document intelligence platform that collects book data, processes it, and enables intelligent question-answering using a Retrieval-Augmented Generation (RAG) pipeline.

The system allows users to:

* Scrape book data automatically
* View book listings
* Ask questions about books
* Get AI-based answers using embeddings and similarity search

---

## Tech Stack

**Backend:**

* Python (Flask)
* ChromaDB (Vector Database)
* Sentence Transformers (Embeddings)
* BeautifulSoup (Web Scraping)

**Frontend:**

* HTML, JavaScript (Single Page Interface)

---

## Features

* Book data scraping from the web
* REST APIs for book retrieval
* RAG-based question answering
* Embedding-based similarity search
* Simple and functional frontend

---

## API Endpoints

| Method | Endpoint | Description             |
| ------ | -------- | ----------------------- |
| GET    | /books   | Retrieve all books      |
| POST   | /scrape  | Scrape and store books  |
| POST   | /ask     | Ask questions using RAG |

---

## How to Run

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs on:

```
http://127.0.0.1:5000
```

---

### Frontend Setup

Open the file directly in your browser:

```
frontend/index.html
```

---

## How to Use

1. Click "Load Books"
2. Wait for books to be scraped
3. Enter a question such as:

   * What are these books about?
   * Suggest similar books
4. View the generated answer

---

## Sample Q&A

**Q:** What are these books about?
**A:** The system retrieves relevant descriptions using embeddings and returns context-based answers.

---

## RAG Pipeline (Simplified)

1. Convert book descriptions into embeddings
2. Store embeddings in ChromaDB
3. Convert user query into embedding
4. Perform similarity search
5. Return relevant context as the answer

---

## Screenshots

Add the following before submission:

* Book listing page
* Question-answer interface
* API response

---

## Project Structure

```
book-insight-ai/
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md
```

---

## Future Improvements

* Integrate OpenAI or other LLM APIs for better responses
* Add book recommendation system
* Improve UI using Tailwind CSS
* Store user query history
* Deploy application to cloud platforms

---

## Author

Naman Phogat

---

## Notes

This project demonstrates full-stack development, AI integration, and implementation of a RAG pipeline in a clean and minimal setup.
