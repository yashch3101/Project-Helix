# Project Helix

> Autonomous AI Engineering Intelligence Platform

Project Helix is an AI-powered Software Engineering Intelligence Platform designed to understand, analyze, reason about, and optimize software systems autonomously.

---

# Current Progress

## Phase 1 — Platform Foundation

- FastAPI Backend
- PostgreSQL Integration
- SQLAlchemy Async ORM
- Alembic Database Migrations
- Dockerized PostgreSQL
- Environment Configuration
- Logging System
- Health Check API

---

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing (Argon2)
- Protected APIs

---

## Project Management

- Create Projects
- Project Ownership
- Project Persistence

---

## Repository Management

- GitHub Repository Import
- Git Repository Cloning
- Local Repository Storage
- Repository Metadata

---

## Repository Intelligence

- Recursive Repository Scanner
- Language Detection
- File Metadata Indexing
- Repository Database Indexing

---

## Code Intelligence

- AST-based Code Parsing
- Function Extraction
- Class Extraction
- Import Detection
- Code Chunk Generation

---

## Embedding Engine

- Code Embedding Generation
- Batch Embedding Pipeline
- PostgreSQL pgvector Storage
- Semantic Code Search

---

## AI Chat Engine

- Chat Sessions
- Conversation History
- History Builder
- Query Rewriter
- Context-aware Retrieval
- RAG Pipeline

# Current Architecture

                    Client
                      │
                      ▼
               FastAPI Backend
                      │
     ┌────────────────┼────────────────┐
     │                │                │
     ▼                ▼                ▼
Authentication   Project APIs    Repository APIs
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
                              Gemini AI Response


# Tech Stack

### AI

- Google Gemini
- Sentence Transformers
- pgvector

### Code Intelligence

- AST Parser
- Semantic Chunking
- Vector Search

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker

### Git

- GitPython

### Database

- PostgreSQL
- pgvector

# Roadmap

## Completed

- Platform Foundation
- Authentication
- Projects
- Repository Import
- Repository Scanner
- AST Code Parser
- Code Chunking
- Embedding Engine
- Semantic Search
- AI Chat Engine
- Conversation Memory
- Query Rewriter
- RAG Retrieval

---

## In Progress

- Citation Engine

---

## Upcoming

- Streaming Responses
- Framework Detection
- Dependency Graph
- Repository Knowledge Graph
- Multi-Agent System
- Autonomous Code Review
- AI Code Generation
- Engineering Memory
- Autonomous Software Architect

# Current Status

| Module | Status |
|---------|--------|
| Platform Foundation | Done |
| Authentication | Done |
| Project Management | Done |
| Repository Management | Done |
| Repository Scanner | Done |
| AST Parser | Done |
| Code Chunking | Done |
| Embedding Engine | Done |
| Semantic Search | Done |
| AI Chat Engine | Done |
| Conversation Memory | Done |
| Query Rewriter | Done |
| Citation Engine | Currently ongoing |
| Streaming Responses | Pending |
| Multi-Agent System | Pending |

---

# Vision

Project Helix aims to become an AI-native software engineering platform capable of:

- Understanding entire software systems
- Building software knowledge graphs
- Detecting architecture automatically
- Performing semantic code search
- Reasoning over repositories using AI
- Acting as an autonomous engineering assistant

# Key Features

- Semantic code search using vector embeddings
- Context-aware AI chat over repositories
- Conversation memory with query rewriting
- AST-based code understanding
- Repository indexing and semantic retrieval
- Scalable RAG pipeline for software engineering