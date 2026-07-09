from src.embeddings import create_embedding
from src.vector_store import qdrant_client


def retrieve_chunks(
    question,
    collection_name,
    top_k=3
):

    if question.strip() == "":
        raise ValueError(
            "Question cannot be empty."
        )

    question_embedding = create_embedding(
        question
    )

    search_response = qdrant_client.query_points(
        collection_name=collection_name,
        query=question_embedding,
        limit=top_k,
        with_payload=True
    )

    retrieved_chunks = []

    for rank, result in enumerate(
        search_response.points,
        start=1
    ):

        chunk_data = {
            "rank": rank,
            "score": result.score,
            "file_name": result.payload["file_name"],
            "chunk_number": result.payload["chunk_number"],
            "text": result.payload["text"]
        }

        retrieved_chunks.append(
            chunk_data
        )

    return retrieved_chunks


def show_retrieved_chunks(retrieved_chunks):

    print("\nRetrieved Chunks")

    if len(retrieved_chunks) == 0:

        print("No relevant chunks were found.")

        return

    for chunk in retrieved_chunks:

        print("\nRank:", chunk["rank"])

        print(
            "Similarity Score:",
            round(chunk["score"], 4)
        )

        print(
            "File Name:",
            chunk["file_name"]
        )

        print(
            "Chunk Number:",
            chunk["chunk_number"]
        )

        print("Text:")
        print(chunk["text"])

        print("-" * 70)