# ⚡ Project Helix

> Autonomous AI Repository Intelligence Platform for understanding, reasoning about, and interacting with large software codebases using Retrieval-Augmented Generation (RAG).

Project Helix is an AI-powered software engineering platform that enables developers to import GitHub repositories and interact with them through natural language. It combines repository parsing, semantic search, AST analysis, vector embeddings, and conversational AI to provide context-aware answers grounded in the source code.

---

# Features

## Repository Intelligence

- Import public GitHub repositories
- Automatic repository cloning
- Recursive repository scanning
- Language detection
- Repository metadata indexing

## Code Intelligence

- AST-based parsing
- Function extraction
- Class extraction
- Import analysis
- Semantic code chunk generation

## AI Knowledge Pipeline

- Code embeddings using Sentence Transformers
- PostgreSQL + pgvector vector storage
- Semantic retrieval
- Context-aware Retrieval-Augmented Generation (RAG)
- Conversation-aware query rewriting
- Persistent chat sessions

## Project Management

- User authentication (JWT)
- Project creation
- Multiple repositories per project
- Repository switching
- Chat history management
- Rename/Delete conversations

---

# System Architecture

```
                     Next.js Frontend
                             │
                             ▼
                     FastAPI Backend
                             │
     ┌───────────────────────┼────────────────────────┐
     │                       │                        │
     ▼                       ▼                        ▼
 Authentication        Project APIs         Repository APIs
                                                  │
                                                  ▼
                                         Repository Scanner
                                                  │
                                                  ▼
                                             AST Parser
                                                  │
                                                  ▼
                                            Code Chunking
                                                  │
                                                  ▼
                                         Embedding Generator
                                                  │
                                                  ▼
                                       PostgreSQL + pgvector
                                                  │
                                                  ▼
                                         Semantic Retrieval
                                                  │
                                                  ▼
                                   Conversation-aware RAG
                                                  │
                                                  ▼
                                            Gemini AI
```

---

# Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Backend

- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic
- Docker

## AI

- Groq
- Sentence Transformers
- pgvector
- RAG Pipeline

## Repository Processing

- GitPython
- Python AST

---

# Project Structure

```text
apps/
├── api/
│   ├── authentication
│   ├── repositories
│   ├── parser
│   ├── retrieval
│   ├── ai
│   ├── chat
│   └── ...
│
└── web/
    ├── app
    ├── components
    ├── services
    └── ...
```

---

# Getting Started

## Backend

```bash
cd apps/api

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
cd apps/web

npm install

npm run dev
```

---

# Current Capabilities

- AI-powered repository understanding
- Semantic code search
- AST-based code intelligence
- Multi-project management
- Repository indexing
- Persistent AI conversations
- Query rewriting with conversation memory
- Vector search using pgvector
- Source-grounded repository answers

---

# Roadmap

### Completed

- Authentication
- Project Management
- Repository Import
- Repository Scanner
- AST Parser
- Semantic Chunking
- Embedding Pipeline
- Vector Search
- AI Chat
- Conversation Memory
- Query Rewriting
- Repository Statistics

### Planned

- Source citations
- Dependency graph visualization
- Framework detection
- Repository knowledge graph
- Multi-agent reasoning
- Autonomous code review
- AI code generation

---

# Vision

Project Helix aims to become an autonomous AI software engineering platform capable of understanding large-scale repositories, reasoning across complex codebases, and assisting developers with architecture exploration, debugging, and software design through conversational AI.

---

# License

MIT License