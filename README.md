# ⚖️ LexiGuard AI Engine v1.0
![Nexus CI Pipeline](https://github.com/Drashtika-Yukti/LexiGuard-AI-Engine/actions/workflows/ci.yml/badge.svg)
![Nexus CD Pipeline](https://github.com/Drashtika-Yukti/LexiGuard-AI-Engine/actions/workflows/cd.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**LexiGuard-AI-Engine** is a production-grade, privacy-first Legal Intelligence platform. It leverages **Agentic RAG** and **Multi-Agent Orchestration** to provide high-fidelity legal reasoning while strictly enforcing data privacy through local PII masking.

---

## 🚀 Key Features
*   **Agentic RAG**: Self-grading retrieval system with hallucination detection.
*   **Privacy Shield**: Local NER-based PII masking via spaCy before cloud transmission.
*   **Elite DevOps**: 3-tier Docker orchestration (FastAPI + React + Go).
*   **Automated Trust**: Integrated RAGAS and DeepEval metrics for legal integrity.
*   **High Speed**: Legal ingestion powered by a high-performance Go microservice.

---

## 🛠️ Architecture
- **Engine**: FastAPI + LangGraph + Groq Llama-3.
- **Frontend**: React + Framer Motion + Glassmorphism UI.
- **Ingestor**: Golang for massive document processing.
- **Database**: Supabase (Vector Store) + SQLite (Session Memory).

---

## ⚙️ CI/CD Pipeline & Deployment Checklist
The project includes a fully automated DevOps pipeline using **GitHub Actions**. To ensure the "Green Signal" in your repository, you must add the following **Secrets**:

1.  `GROQ_API_KEY`
2.  `COHERE_API_KEY`
3.  `SUPABASE_URL`
4.  `SUPABASE_SERVICE_ROLE_KEY`

---

## 🛡️ Trust & Evaluation Layer
Check the **GitHub Actions** logs after each push to see the latest "Legal Integrity Scores":
*   **RAGAS**: Faithfulness & Context Precision.
*   **DeepEval**: Assertive legal unit testing.
*   **LangSmith**: Complete observability and decision tracing.

---

## 📦 Local Launch
```powershell
docker-compose up --build
```
- **Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

---

## 📜 License
This project is for professional enterprise use and adheres to strict data privacy standards. MIT Licensed.
