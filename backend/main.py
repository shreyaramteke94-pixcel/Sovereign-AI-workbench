import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

from backend.llm import ask_llm
from backend.agent import run_agent
from backend.rag import add_document
from backend.audit import read_audit


# =========================================
# FASTAPI APPLICATION
# =========================================

app = FastAPI(
    title="Sovereign AI Workbench",
    description="On-Premise Agentic AI Prototype",
    version="0.1.0"
)


# =========================================
# CORS CONFIGURATION
# =========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "null",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================================
# DOCUMENT STORAGE
# =========================================

DOCUMENT_FOLDER = "./data/documents"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# =========================================
# DEMO AUTHENTICATION
# =========================================

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"


@app.post("/login")
def login(
    username: str,
    password: str
):

    if (
        username == DEMO_USERNAME
        and password == DEMO_PASSWORD
    ):

        return {
            "success": True,
            "message": "Login successful",
            "username": username
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "system": "Sovereign AI Workbench",
        "status": "running",
        "mode": "on-premise"
    }


# =========================================
# DIRECT LOCAL AI
# =========================================

@app.get("/ask")
def ask(question: str):

    answer = ask_llm(question)

    return {
        "question": question,
        "answer": answer
    }


# =========================================
# AGENT
# =========================================

@app.get("/agent")
def agent(task: str):

    result = run_agent(task)

    return {
        "task": task,
        "agent_result": result
    }


# =========================================
# DOCUMENT UPLOAD
# =========================================

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        return {
            "error": "Only PDF files are supported."
        }

    file_path = os.path.join(
        DOCUMENT_FOLDER,
        file.filename
    )

    file_data = await file.read()

    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(
            file_data
        )


    # =====================================
    # EXTRACT PDF TEXT
    # =====================================

    reader = PdfReader(
        file_path
    )

    extracted_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            extracted_text += (
                page_text + "\n"
            )


    # =====================================
    # SAVE EXTRACTED TEXT
    # =====================================

    text_file_path = os.path.splitext(
        file_path
    )[0] + ".txt"

    with open(
        text_file_path,
        "w",
        encoding="utf-8"
    ) as text_file:

        text_file.write(
            extracted_text
        )


    # =====================================
    # INDEX DOCUMENT INTO CHROMADB
    # =====================================

    result = add_document(
        text_file_path
    )


    return {
        "message":
            "Document uploaded and indexed successfully.",

        "filename":
            file.filename,

        "pages":
            len(reader.pages),

        "chunks":
            result["chunks"]
    }

# =========================================
# DOCUMENT LIST
# =========================================

@app.get("/documents")
def documents():

    files = []

    for filename in os.listdir(DOCUMENT_FOLDER):

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        if os.path.isfile(file_path):

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in [".pdf", ".txt"]:

                files.append({
                    "filename": filename,
                    "type": extension.replace(".", "").upper(),
                    "size": os.path.getsize(file_path)
                })

    return {
        "documents": files
    }


# =========================================
# SECURITY STATUS
# =========================================

@app.get("/security/status")
def security_status():

    return {

        "inference": {

            "status": "LOCAL",

            "model": "Qwen 2.5 3B",

            "provider": "Ollama"
        },


        "embeddings": {

            "status": "LOCAL",

            "model": "Nomic Embed Text",

            "provider": "Ollama"
        },


        "vector_database": {

            "status": "LOCAL",

            "database": "ChromaDB"
        },


        "data_mode": {

            "status": "PRIVATE",

            "storage": "Local filesystem"
        },


        "external_ai_api": {

            "status": "NOT CONFIGURED"
        },


        "audit_logging": {

            "status": "ENABLED",

            "storage": "Local JSONL log"
        },


        "authentication": {

            "status": "ENABLED",

            "mode": "Prototype"
        }
    }

# =========================================
# SYSTEM EVALUATION
# =========================================

@app.get("/evaluation")
def evaluation():

    logs = read_audit(1000)

    total_tasks = len(logs)

    successful_tasks = 0
    policy_checks = 0
    rag_tasks = 0

    for log in logs:

        trace = log.get("trace", [])

        if "Final answer generated" in trace:
            successful_tasks += 1

        if "Agent identified a policy/compliance task" in trace:
            policy_checks += 1

        if "Searching private knowledge base" in trace:
            rag_tasks += 1

    success_rate = 0

    if total_tasks > 0:
        success_rate = round(
            (successful_tasks / total_tasks) * 100,
            1
        )

    return {
        "total_tasks": total_tasks,
        "successful_tasks": successful_tasks,
        "success_rate_percent": success_rate,
        "policy_checks": policy_checks,
        "rag_tasks": rag_tasks,
        "external_ai_api": "NOT CONFIGURED",
        "inference": "LOCAL",
        "embeddings": "LOCAL",
        "vector_database": "LOCAL"
    }
# =========================================
# AUDIT LOG
# =========================================

@app.get("/audit")
def audit():

    return {
        "logs": read_audit(20)
    }

    # =========================================
# PRIVATE DOCUMENTS
# =========================================

@app.get("/documents")
def list_documents():

    documents = []

    if not os.path.exists(DOCUMENT_FOLDER):
        return {
            "documents": []
        }

    for filename in os.listdir(DOCUMENT_FOLDER):

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        if os.path.isfile(file_path):

            documents.append({
                "filename": filename,
                "type": os.path.splitext(filename)[1].replace(".", "").upper(),
                "size": os.path.getsize(file_path)
            })

    return {
        "documents": documents
    }