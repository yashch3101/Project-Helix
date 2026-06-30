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

## Authentication Module

- User Registration
- User Login
- JWT Authentication
- Password Hashing (Argon2)
- Protected Routes
- Swagger Authorization

---

## Project Management

- Create Project
- Project Persistence
- Project APIs
- Project Ownership

---

## Repository Management

- Import GitHub Repository
- Git Repository Cloning
- Repository Metadata Storage
- Local Repository Storage

---

## Repository Scanner (Foundation)

- Repository File Indexing
- Recursive File Scanning
- Language Detection
- Repository Metadata Extraction
- File Metadata Database

---

# Current Architecture

```
Client
   │
   ▼
FastAPI API
   │
   ├── Authentication
   ├── Projects
   ├── Repository Import
   └── Scanner Engine
          │
          ▼
PostgreSQL
```

---

# Tech Stack

### Backend

- FastAPI
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- AsyncPG
- PostgreSQL
- Docker

### Authentication

- JWT
- Pwdlib (Argon2)

### Git

- GitPython

### Database

- PostgreSQL

---

# Roadmap

## Completed

- Platform Foundation
- Authentication
- Projects
- Repository Import
- Repository Scanner V1

## In Progress

- Repository Intelligence Engine

## Upcoming

- Framework Detection
- Dependency Analyzer
- AST Parser
- Neo4j Knowledge Graph
- Qdrant Vector Database
- AI Engineering Agent
- Autonomous Code Understanding
- Multi-Agent System
- RAG Pipeline
- Engineering Memory
- Autonomous Software Architect

---

# Current Status

| Module | Status |
|---------|--------|
| Platform Foundation | Done |
| Authentication | Done |
| Project Management | Done |
| Repository Management | Done |
| Repository Scanner | Done |
| Framework Detection | ⏳ |
| AST Parser | ⏳ |
| Knowledge Graph | ⏳ |
| AI Engine | ⏳ |

---

# Vision

Project Helix aims to become an AI-native software engineering platform capable of:

- Understanding entire software systems
- Building software knowledge graphs
- Detecting architecture automatically
- Performing semantic code search
- Reasoning over repositories using AI
- Acting as an autonomous engineering assistant