# Dev-Env Platform

A cloud-native **Internal Developer Platform (IDP)** that scans developer environments, analyzes readiness, and provides visibility via automated scoring and dashboards.

---

## 🎯 Goal

- Learn AWS deeply by building real systems
- Solve developer onboarding and environment issues
- Build a production-style internal platform
- Prepare for Cloud / DevOps / Platform Engineering roles

---

## 🏗️ High-Level Architecture

CLI
→ FastAPI Backend
→ S3 (raw scans)
→ DynamoDB (summaries)
→ EventBridge
→ Lambda (analysis & scoring)
→ CloudWatch / SNS
→ React Dashboard


---

## 📁 Repo Structure (Current)

backend/
└── app/
└── main.py


---

## 📅 Progress Log

### Day 1 — Design
- Defined product scope and real-world problems
- Designed cloud-native, event-driven architecture
- Created data contracts and readiness scoring model

### Day 2 — Backend Foundation
- Initialized FastAPI backend
- Set up dependency management
- Added `/health` endpoint
- Verified API via Swagger UI
- Committed backend foundation to GitHub

---

## 🧠 Tech Stack (So Far)

- FastAPI (Python)
- Uvicorn (ASGI)
- Git & GitHub
- AWS (planned)
- React (planned)

---

## 🚀 Status

🟢 Backend foundation complete  
🟡 Data ingestion in progress

### Day 3 — Scan Ingestion (Backend Becomes Functional)
- Defined scan data contract using Pydantic models
- Added `POST /scan` endpoint to accept environment scans
- Implemented automatic request validation for nested scan data
- Verified ingestion and validation using Swagger UI

Day 4 — Scan Storage Preparation (Persistence Added)
Introduced a service layer to handle scan persistence
Designed an S3-ready local storage structure for raw scan data
Implemented immutable, timestamp-based JSON storage for scans
Connected the POST /scan endpoint to the storage service
Ensured safe serialization of validated scan data (including datetime fields)
Verified end-to-end flow: ingest → validate → persist



