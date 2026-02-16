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

Day 5 – Backend Storage Integration & Scan Upload Flow
🎯 Objective
Integrate persistent storage into the FastAPI backend so validated developer environment scans can be saved reliably, with support for both local filesystem storage and AWS S3 — without changing API behavior.
🧱 What Was Implemented
FastAPI backend with a clean service-layer architecture
Pydantic v2 models with strict request validation
Storage abstraction layer:
LocalStorage → saves scans as JSON files
S3Storage → uploads scans directly to AWS S3
Pluggable storage backend controlled via environment variable:
STORAGE_BACKEND=local | s3
Consistent object structure:
scans/<developer_id>/<timestamp>.json
☁️ AWS S3 Integration
Created an S3 bucket for scan storage
Configured a least-privilege IAM user with:
s3:PutObject access to scans/*
Used boto3 to upload JSON scan data
Credentials loaded via environment variables (no hardcoding)
🛠 Key Fixes & Learnings
Fixed Python version issues by standardizing on Python 3.11
Resolved circular imports and package resolution errors
Enforced strict separation of:
Application code (backend/app)
Runtime data (storage/scans)
Learned proper Pydantic v2 JSON serialization using:
model_dump(mode="json")
Debugged and fixed service ↔ storage method signature mismatches
Handled datetime serialization safely using ISO 8601 strings
✅ Current Status
/health endpoint working
/scan endpoint:
Validates nested request schema
Saves scan data successfully (local or S3)
Backend is stable, cloud-ready, and extensible

🟦 Day 6 — DynamoDB Scan Metadata Storage
Designed a DynamoDB table to store scan summaries (metadata) using user_id as partition key and scan_id as sort key
Implemented a dedicated DynamoDB storage layer to save and query scan metadata
Stored lightweight fields like status (PASS/FAIL), OS, and timestamp for fast access
Used Query (not Scan) to efficiently fetch scan history for a user
Applied least-privilege IAM permissions for DynamoDB access
Kept full scan data in S3/local while DynamoDB handles queryable summaries

Day 7 – AWS Cognito Authentication
Created AWS Cognito User Pool for user management
Configured Hosted UI with Authorization Code flow
Generated access tokens using OAuth 2.0
Integrated JWT verification in FastAPI backend
Implemented RS256 signature validation using Cognito JWKS
Verified token issuer, token_use=access, and client_id
Protected /scan/history using HTTP Bearer authentication
Enforced role-based access control using Cognito groups (admins)


Day 8 – Cognito PKCE + Secure Full-Stack Integration

Implemented AWS Cognito OAuth2 Authorization Code Flow with PKCE in the React frontend for secure authentication.
Integrated FastAPI backend with RS256 JWT verification using Cognito JWKS and validated issuer, token type, and client ID.
Protected /scan/history endpoint to allow access only to authenticated users with valid access tokens.
Connected frontend to backend using Bearer tokens and successfully displayed protected scan history in the UI.
Added logout functionality and completed secure end-to-end authentication architecture.

