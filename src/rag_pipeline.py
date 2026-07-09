from src.ingestion import load_documents
from src.chunking import chunk_all_documents
from src.embeddings import create_embeddings_for_chunks

from src.vector_store import (
    collection_exists,
    get_stored_point_count,
    create_collection,
    store_chunks
)


def prepare_rag_database(
    collection_name,
    chunk_size=500,
    chunk_overlap=50,
    rebuild=False
):

    documents = load_documents()

    chunks = chunk_all_documents(
        documents=documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    expected_chunk_count = len(chunks)

    print(
        "Expected number of points:",
        expected_chunk_count
    )

    if collection_exists(collection_name):

        stored_point_count = get_stored_point_count(
            collection_name
        )

        print(
            "Existing points in Qdrant:",
            stored_point_count
        )

        if (
            stored_point_count == expected_chunk_count
            and rebuild is False
        ):

            print("Collection is already complete.")
            print("Embedding API calls were skipped.")

            return chunks

    chunks_with_embeddings = create_embeddings_for_chunks(
        chunks
    )

    if len(chunks_with_embeddings) == 0:

        raise ValueError(
            "No embeddings were created."
        )

    vector_size = len(
        chunks_with_embeddings[0]["embedding"]
    )

    print(
        "Detected vector size:",
        vector_size
    )

    create_collection(
        collection_name=collection_name,
        vector_size=vector_size,
        recreate=True
    )

    store_chunks(
        collection_name=collection_name,
        chunks_with_embeddings=chunks_with_embeddings
    )

    print("RAG database preparation completed.")

    return chunks