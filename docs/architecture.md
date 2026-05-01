# Aegis Legal AI: System Architecture Whitepaper

## 1. Executive Summary
Aegis Legal AI is a production-grade intelligence engine designed for high-stakes legal reasoning. It combines state-of-the-art **Agentic RAG** with a robust **Privacy Shield** to ensure that data remains secure while providing high-fidelity legal insights.

## 2. Core Architecture
The system follows a **Monorepo Microservices** architecture, designed for horizontal scalability and high availability.

### 2.1 The Intelligence Engine (`engine/`)
Built with **FastAPI** and **LangGraph**, the engine orchestrates a multi-agent flow:
- **Privacy Guard**: Local PII scrubbing using spaCy NER before any data leaves the secure environment.
- **Agentic RAG**: A self-correcting retrieval system that grades context relevance and judges hallucinations in real-time.
- **Memory Layer**: Stateless conversation persistence backed by **Supabase (Postgres)**.

### 2.2 Aegis Studio (`studio/`)
A premium legal workspace built with **React** and **Vite**. It features:
- **Solid Enterprise UI**: High-trust, high-contrast dark mode.
- **Cognitive Trace**: Real-time transparency into the AI's reasoning steps.
- **Consolidated API Client**: Robust, error-aware communication with the engine.

### 2.3 Worker Layer (`workers/`)
- **Go Ingestor**: A high-performance Golang microservice designed for massive legal document processing and vectorization.

## 3. Data Privacy & Security
Aegis implements a "Privacy First" policy:
- **Local Masking**: All PII (Names, Addresses, Dates) is replaced with tokens locally.
- **Encrypted Vectors**: Document embeddings are stored in **Supabase pgvector** with strict row-level security (RLS).
- **Stateless Execution**: The engine does not store sensitive query data locally; all persistence is handled via secure, encrypted cloud databases.

## 4. Trust & Evaluation
Trust is verified through continuous benchmarking:
- **RAGAS**: Continuous monitoring of Faithfulness and Context Precision.
- **DeepEval**: Assertive unit testing for legal compliance.

---
*© 2026 Aegis Legal AI. Enterprise-Grade Legal Intelligence.*
