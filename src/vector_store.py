from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from src.config import QDRANT_FOLDER


QDRANT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


qdrant_client = QdrantClient(
    path=str(QDRANT_FOLDER)
)


def collection_exists(collection_name):

    exists = qdrant_client.collection_exists(
        collection_name=collection_name
    )

    return exists


def get_stored_point_count(collection_name):

    if not collection_exists(collection_name):
        return 0

    result = qdrant_client.count(
        collection_name=collection_name,
        exact=True
    )

    return result.count


def create_collection(
    collection_name,
    vector_size,
    recreate=False
):

    already_exists = collection_exists(
        collection_name
    )

    if already_exists and recreate:

        qdrant_client.delete_collection(
            collection_name=collection_name
        )

        print("Old collection deleted.")

        already_exists = False

    if already_exists:

        print(
            "Collection already exists:",
            collection_name
        )

        return

    qdrant_client.create_collection(
        collection_name=collection_name,

        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    print(
        "Collection created:",
        collection_name
    )


def store_chunks(
    collection_name,
    chunks_with_embeddings
):

    if len(chunks_with_embeddings) == 0:

        raise ValueError(
            "No chunks with embeddings were provided."
        )

    points = []

    for chunk in chunks_with_embeddings:

        point = PointStruct(
            id=chunk["id"],

            vector=chunk["embedding"],

            payload={
                "file_name": chunk["file_name"],
                "chunk_number": chunk["chunk_number"],
                "text": chunk["text"]
            }
        )

        points.append(point)

    qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )

    stored_point_count = get_stored_point_count(
        collection_name
    )

    print(
        "Total points stored in Qdrant:",
        stored_point_count
    )


def close_qdrant_client():

    qdrant_client.close()

    print("Qdrant client closed successfully.")