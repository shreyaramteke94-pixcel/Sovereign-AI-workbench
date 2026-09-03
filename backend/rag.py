import os
import re
import requests
import chromadb


OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"

VECTOR_DB_PATH = "./data/vectorstore"


client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = client.get_or_create_collection(
    name="private_documents"
)


def create_embedding(text: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


def split_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def add_document(file_path: str):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    if not text.strip():

        return {
            "document": os.path.basename(file_path),
            "chunks": 0
        }

    chunks = split_text(text)

    document_name = os.path.basename(file_path)

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        chunk_id = (
            f"{document_name}_chunk_{index}"
        )

        ids.append(chunk_id)

        documents.append(chunk)

        embeddings.append(embedding)

        metadatas.append(
            {
                "source": document_name,
                "chunk": index
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "document": document_name,
        "chunks": len(chunks)
    }


def get_keywords(text: str):

    words = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        text.lower()
    )

    stop_words = {
        "the",
        "and",
        "for",
        "are",
        "was",
        "were",
        "with",
        "from",
        "that",
        "this",
        "have",
        "has",
        "how",
        "what",
        "when",
        "where",
        "which",
        "can",
        "could",
        "would",
        "should",
        "does",
        "employee",
        "employees"
    }

    return set(
        word
        for word in words
        if word not in stop_words
    )


def calculate_keyword_score(
    query: str,
    document: str
):

    query_words = get_keywords(query)

    document_words = get_keywords(document)

    if not query_words:
        return 0.0

    overlap = (
        query_words.intersection(document_words)
    )

    return len(overlap) / len(query_words)


def search_documents(
    query: str,
    number_of_results: int = 5
):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []
    relevance_scores = []

    for index, document in enumerate(documents):

        keyword_score = calculate_keyword_score(
            query,
            document
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        # A document must have at least
        # some meaningful keyword overlap.
        #
        # This prevents unrelated documents
        # from automatically being treated
        # as relevant.

        if keyword_score >= 0.15:

            filtered_documents.append(
                document
            )

            if index < len(metadatas):
                filtered_metadatas.append(
                    metadatas[index]
                )
            else:
                filtered_metadatas.append({})

            filtered_distances.append(
                distance
            )

            relevance_scores.append(
                keyword_score
            )

    return {
        "documents": [
            filtered_documents
        ],
        "metadatas": [
            filtered_metadatas
        ],
        "distances": [
            filtered_distances
        ],
        "relevance_scores": [
            relevance_scores
        ]
    }