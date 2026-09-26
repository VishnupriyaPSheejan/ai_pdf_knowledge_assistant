# Deployment Guide

## Docker

1. Create `.env` from `.env.example`.
2. Add your LLM API key.
3. Run `docker compose up --build`.
4. Open Streamlit on port 8501.

## Single-service cloud deployment

The included Dockerfile starts the FastAPI API. For a simple cloud deployment, deploy the API container and expose port 8000. Then deploy Streamlit separately and set:

```text
API_URL=https://YOUR-API-DOMAIN
```

## Production architecture

For a production portfolio version, use:

```text
Streamlit / React
      |
      v
FastAPI
      |
      +---- Object Storage (PDFs)
      |
      +---- PostgreSQL (metadata/users)
      |
      +---- Qdrant / pgvector (vectors)
      |
      +---- LLM API
```

Add authentication, rate limiting, file-size limits, malware scanning, logging and HTTPS before exposing it to arbitrary users.
