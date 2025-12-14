# Document QA Application

AI-powered document question answering system using RAG (Retrieval Augmented Generation).

## Features
- PDF document upload and processing
- Semantic search with vector embeddings
- LLM-based question answering
- Agent-based workflow with LangGraph
- Web UI for easy interaction

## Technology Stack
- **LLM:** Ollama (Llama 3.2)
- **Vector DB:** Weaviate v1.27.6
- **Framework:** FastAPI + LangGraph
- **Embeddings:** Sentence Transformers
- **Frontend:** HTML/CSS/JavaScript

## Quick Start

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum
- 10GB free disk space

### Installation

1. Clone repository

2. Start application

3. Wait 1 minute for services to start

4. Access application

http://localhost:8000

### Usage

1. Upload a PDF document via the web UI
2. Wait for processing (chunking and embedding)
3. Ask questions about the document
4. Get AI-generated answers

