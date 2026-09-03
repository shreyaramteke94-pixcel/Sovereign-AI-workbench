import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag import add_document


document = PROJECT_ROOT / "data" / "documents" / "company_policy.txt"

document_id = add_document(str(document))

print(f"Document added successfully: {document_id}")