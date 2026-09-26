# AI PDF Knowledge Assistant

An end-to-end LLM-powered chatbot that lets users upload their own PDF documents and ask questions grounded in those documents. The application uses RAG (Retrieval-Augmented Generation), hybrid retrieval, conversational memory, source citations, and a FastAPI + Streamlit architecture.

## Features

- Upload one or more PDFs and build a searchable knowledge base
- Automatic PDF text extraction with page numbers
- Chunking with overlap and metadata
- Local semantic embeddings using Sentence Transformers
- FAISS vector index for fast retrieval
- Optional keyword retrieval using BM25
- Hybrid retrieval + score fusion
- LLM answer generation using OpenAI-compatible chat models
- Answers include document name and page citations
- Conversation memory for follow-up questions
- Prompt designed to reduce hallucination: answer only from retrieved context
- FastAPI backend
- Streamlit frontend
- Docker support
- Health endpoint
- Basic unit tests
- Configurable through `.env`

## Architecture

```text
PDFs
  |
  v
PyMuPDF extraction
  |
  v
Chunking + metadata
  |
  +------------------+
  |                  |
  v                  v
Embeddings         BM25
  |                  |
  v                  v
FAISS index       Keyword index
  |                  |
  +--------+---------+
           |
           v
      Hybrid Retrieval
           |
           v
   Conversation Context
           |
           v
     LLM Generation
           |
           v
 Answer + Page Citations
```

## Tech stack

- Python 3.11+
- FastAPI
- Streamlit
- OpenAI-compatible LLM API
- Sentence Transformers
- FAISS
- rank-bm25
- PyMuPDF
- Pydantic
- Docker

## Project structure

```text
ai-pdf-knowledge-assistant/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── rag/
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── index.py
│   │   └── pipeline.py
│   ├── services/
│   │   ├── pdf_service.py
│   │   └── llm_service.py
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── tests/
├── data/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 1. Local setup

```bash
git clone <your-repository-url>
cd ai-pdf-knowledge-assistant
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

```bash
cp .env.example .env
```

Then start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL shown by the terminal.

## 2. Using the application

1. Open the Streamlit UI.
2. Upload one or more PDFs.
3. Click **Index documents**.
4. Ask a question.
5. Review the answer and source pages.
6. Ask follow-up questions; the current session remembers recent turns.

## 3. API endpoints

### Health

`GET /health`

### Upload and index

`POST /documents/index`

Multipart form field:

`files`: one or more PDF files.

### Chat

`POST /chat`

Example body:

```json
{
  "question": "What is the main purpose of this document?",
  "history": [
    {"role": "user", "content": "Give me a short summary."},
    {"role": "assistant", "content": "The document describes..."}
  ]
}
```

## 4. Customization

This project is intentionally designed so you can turn it into a specialized assistant.

Examples:

- HR policy assistant
- Automotive engineering assistant
- Financial report assistant
- Legal document assistant
- Research-paper assistant
- Company knowledge assistant
- MBA study assistant

The main customization happens through your PDFs. You can also customize the system prompt in `app/services/llm_service.py` and retrieval settings in `.env`.

## 5. Deployment

### Option A — Docker

Build and run:

```bash
docker compose up --build
```

The API runs on port 8000 and Streamlit on port 8501.

### Option B — Render / Railway / any Docker host

Deploy the repository using the included `Dockerfile`. Set these environment variables in the hosting provider:

```text
OPENAI_API_KEY=your_key
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=6
CHUNK_SIZE=800
CHUNK_OVERLAP=120
```

For a production deployment, use persistent storage for the `data/` directory or replace FAISS persistence with a managed vector database such as Qdrant, Pinecone, or pgvector.

## Important deployment note

The included version is a portfolio/development deployment. It stores the FAISS index and uploaded files locally. On ephemeral cloud instances, local files can disappear after a redeploy. For a production-grade version, move document storage to object storage and the vector index to a persistent vector database.

## Evaluation

The repository includes a small retrieval test suite. For a stronger portfolio version, create a 30–50 question evaluation set from your own PDFs and measure:

- Recall@K
- MRR
- Context precision
- Context recall
- Answer faithfulness
- Answer relevance

## Security notes

- Never commit `.env` or API keys.
- Do not upload confidential company documents to a personal deployment without authorization.
- Treat uploaded documents as untrusted input.
- Add authentication and rate limiting before exposing the API publicly.

## Suggested GitHub description

> LLM-powered PDF Knowledge Assistant using RAG, hybrid retrieval, FAISS, Sentence Transformers, conversational memory, source citations, FastAPI, Streamlit, and Docker.
