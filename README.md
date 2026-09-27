# Sovereign On-Premise Agentic AI Workbench

A secure, privacy-focused enterprise AI workbench that enables organizations to run AI agents, private knowledge retrieval, enterprise policy checks, and AI-assisted workflows within their own infrastructure.

---

## 📌 Project Overview

The Sovereign On-Premise Agentic AI Workbench is designed for organizations that want to use AI while maintaining control over sensitive data, AI processing, infrastructure, and operational logs.

Unlike a conventional cloud-based chatbot, this prototype uses locally hosted AI models and a local vector database so that enterprise documents can remain within the organization's controlled environment.

The system provides a unified workspace for:

- Local AI inference
- Private document retrieval
- Agentic task execution
- Enterprise policy and compliance checks
- Tool-based calculations
- Document indexing
- Source evidence
- Security status monitoring
- Audit logging
- System evaluation

---

## 🎯 Problem Statement

Organizations increasingly use AI for document analysis, decision support, and automation.

However, sensitive enterprise information may create challenges when AI processing depends on external cloud AI services.

Examples of sensitive information include:

- Company policies
- Internal documents
- Security procedures
- Confidential business information
- Employee information
- Organizational knowledge

The project addresses this problem by providing an AI workbench where AI processing and private knowledge retrieval can operate locally.

---

## 💡 Proposed Solution

The system combines:

1. Local Large Language Model
2. Local document embeddings
3. Private Retrieval-Augmented Generation (RAG)
4. Agentic task routing
5. Enterprise policy evaluation
6. Local vector database
7. Audit logging
8. Security and privacy monitoring

The agent determines the appropriate capability for a task and then retrieves private knowledge or uses an available tool.

---

## 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
              Web Dashboard
                      │
                      ▼
                FastAPI Backend
                      │
                      ▼
             Agentic Orchestrator
                /           \
               /             \
              ▼               ▼
       Private RAG          Tools
          │                   │
          ▼                   ▼
      ChromaDB            Calculator
          │
          ▼
   Nomic Embed Text
          │
          ▼
   Private Documents
          │
          └──────────────┐
                         ▼
                  Local LLM
                  Qwen 2.5 3B
                    Ollama
                         │
                         ▼
                Verified Response
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Source Evidence          Audit Log


       🔐 Sovereignty & Privacy

The prototype is designed around local AI processing.

Local Components
Qwen 2.5 3B — local AI inference
Ollama — local model runtime
Nomic Embed Text — local document embeddings
ChromaDB — local vector database
Local filesystem — document storage
Local JSONL — audit logging
External AI API

No external AI API is configured in the prototype.

This allows the demonstration to show how enterprise documents can be processed using locally hosted AI components.

🤖 Agentic Capabilities

The workbench supports multiple task types.

1. Private Knowledge Retrieval

The agent searches indexed private documents and uses relevant information to answer questions.

Example:

How many days can employees work remotely?

The agent retrieves the relevant company policy and generates an answer using the retrieved information.

2. Calculator Tool

The agent can identify mathematical tasks and use the calculator capability.

Example:

Calculate 125 * 48

Expected result:

6000
3. Enterprise Policy / Compliance Check

The agent can identify policy-related requests and evaluate them against private organizational policies.

Example:

Can an employee work remotely for 4 days?

The system retrieves the relevant policy and evaluates the request according to the organization's policy.

Another example:

Can I upload confidential company documents
to my personal Google Drive?

The system retrieves the relevant private security policy and evaluates the request.

4. Hallucination Protection

If relevant information cannot be found in the private knowledge base, the system avoids intentionally inventing organizational information.

Instead, it can return a response such as:

I couldn't find relevant information
in the private knowledge base.

This helps keep enterprise responses grounded in available organizational information.

📄 Document Processing

The workbench supports PDF document upload and local indexing.

The processing pipeline is:

PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Text Chunking
    │
    ▼
Local Embedding
    │
    ▼
ChromaDB
    │
    ▼
Private Knowledge Retrieval

Uploaded documents are stored locally and indexed for retrieval.

🔎 Retrieval-Augmented Generation

The RAG pipeline uses:

Nomic Embed Text
ChromaDB
Local document chunks
Qwen 2.5 3B
Ollama

The system first retrieves relevant private information and then provides the retrieved context to the local language model.

This allows responses to be grounded in organizational documents instead of relying only on the model's pretrained knowledge.

📋 Audit Logging

Agent activity is recorded locally.

The audit system records information such as:

Timestamp
User task
Agent execution trace
Final answer

Example execution flow:

Task Received
      ↓
Task Type Identified
      ↓
Private Knowledge Searched
      ↓
Relevant Evidence Retrieved
      ↓
Local AI Generation
      ↓
Final Answer
      ↓
Audit Record

The audit records are stored locally in JSONL format.

📊 System Evaluation

The prototype provides a system evaluation endpoint and dashboard metrics based on actual locally stored agent activity.

The evaluation includes:

Total agent tasks
Successful tasks
Success rate
Policy checks
RAG tasks
External AI API status

The metrics are generated from actual system activity rather than manually entered values.

🔒 Security & Privacy Dashboard

The dashboard provides visibility into the current AI environment.

The system can display:

Inference status
Embedding status
Vector database status
Data storage status
External AI API status
Audit logging status

Example:

Inference          → LOCAL
Embeddings         → LOCAL
Vector Database    → LOCAL
Data Storage       → PRIVATE
External AI API    → NOT CONFIGURED
Audit Logging      → ENABLED
🖥️ Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
FastAPI
Uvicorn
REST APIs
AI
Qwen 2.5 3B
Ollama
Embeddings
Nomic Embed Text
Ollama
RAG / Vector Database
Retrieval-Augmented Generation
ChromaDB
Document Processing
PyPDF
Security & Governance
Prototype authentication
Local data storage
Audit logging
Policy/compliance evaluation
Source evidence
📁 Project Structure
sovereign-ai-workbench/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── llm.py
│   ├── rag.py
│   ├── tools.py
│   ├── audit.py
│   ├── index_document.py
│   └── test_rag.py
│
├── frontend/
│   └── index.html
│
├── data/
│   └── documents/
│
├── logs/
│
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Requirements

Before running the project, install:

Python 3.12+
Ollama
Git

The following Ollama models are required:

qwen2.5:3b
nomic-embed-text:latest
🚀 Installation
1. Clone the Repository
git clone https://github.com/shreyaramteke94-pixcel/Sovereign-AI-Workbench.git

Move into the project:

cd Sovereign-AI-Workbench
2. Create a Virtual Environment
python -m venv venv

Activate the environment on Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Install / Start Ollama

Make sure Ollama is installed and running.

Check the available models:

ollama list

Required models:

qwen2.5:3b
nomic-embed-text:latest

If required, download them using:

ollama pull qwen2.5:3b
ollama pull nomic-embed-text
▶️ Running the Backend

From the project root:

python -m uvicorn backend.main:app --reload

Backend address:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
🌐 Running the Frontend

Open another terminal and activate the virtual environment if required.

Run:

python -m http.server 5500 --directory frontend

Open the dashboard:

http://127.0.0.1:5500
🔑 Prototype Login

The current prototype uses:

Username: admin
Password: admin123

These credentials are intended for demonstration purposes only.

For production deployment, enterprise identity management and stronger authentication should be implemented.

🧪 Demo Scenarios
Demo 1 — Private RAG

Ask:

How many days can employees work remotely?

The agent searches the private knowledge base and retrieves the relevant company policy.

Demo 2 — Policy Compliance

Ask:

Can an employee work remotely for 4 days?

The system identifies this as a policy-related task, retrieves the relevant policy, and evaluates the request.

Demo 3 — Security Policy

Ask:

Can I upload confidential company documents
to my personal Google Drive?

The system retrieves the private security policy and evaluates the request.

Demo 4 — Calculator

Ask:

Calculate 125 * 48

The agent identifies the calculation task and uses the calculator capability.

Expected result:

6000
Demo 5 — Unknown Information

Ask a question that is not covered by the private documents.

The system should avoid presenting unsupported organizational information and can indicate that relevant private information was not found.

🛡️ Security Design Principles

The prototype demonstrates the following principles:

Local AI inference
Local document storage
Local vector database
No configured external AI API
Authentication
Audit logging
Policy-based evaluation
Source evidence
Knowledge-grounded responses
Visibility into AI infrastructure
📈 Agent Execution Trace

The dashboard exposes the agent's execution process.

Example:

Task received
Agent identified a policy/compliance task
Searching private policy knowledge base
Relevant documents found
Context accepted
Relevant policy evidence identified
Evaluating request against organizational policy
Generating final answer with local AI
Policy compliance evaluation completed
Final answer generated

This provides transparency into how the agent handled the task.

🔮 Future Enhancements

The current prototype can be extended with:

Advanced agent orchestration using LangGraph
Enterprise Role-Based Access Control
Keycloak-based identity management
JWT-based authentication
Stronger AI guardrails
OCR for scanned documents
Larger local language models
Qdrant or Milvus for scalable vector storage
Docker deployment
Kubernetes / K3s deployment
OpenTelemetry-based observability
Prometheus and Grafana monitoring
Human approval workflows
Additional enterprise tools
Multi-agent workflows

These are future extensions and are not represented as implemented features of the current prototype.

🎯 Project Objective

The objective of the Sovereign On-Premise Agentic AI Workbench is to demonstrate how organizations can use agentic AI capabilities while maintaining greater control over:

Private organizational data
AI processing
Infrastructure
Knowledge retrieval
AI operations
Audit records

The prototype demonstrates a local-first approach to enterprise AI using private RAG, local AI inference, agentic task routing, policy evaluation, and auditability.

👩‍💻 Project

Sovereign On-Premise Agentic AI Workbench

Core Concepts
Sovereign AI
     +
On-Premise AI
     +
Agentic AI
     +
Private RAG
     +
Enterprise Governance
     +
Auditability
📌 Disclaimer

This repository is an academic and innovation prototype.

The authentication, security controls, and policy evaluation mechanisms are intended for demonstration purposes and should be strengthened before use in a real production enterprise environment.