from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.config import EMBEDDING_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text]
    )

    embedding_vector = response.data[0].embedding

    return embedding_vector


def create_embeddings_for_chunks(chunks):

    print("Creating embeddings for all chunks...")

    chunk_texts = []

    for chunk in chunks:
        chunk_texts.append(chunk["text"])

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=chunk_texts
    )

    chunks_with_embeddings = []

    for chunk, embedding_result in zip(
        chunks,
        response.data
    ):

        chunk_with_embedding = {
            "id": chunk["id"],
            "file_name": chunk["file_name"],
            "chunk_number": chunk["chunk_number"],
            "text": chunk["text"],
            "embedding": embedding_result.embedding
        }

        chunks_with_embeddings.append(
            chunk_with_embedding
        )

    print(
        "Total embeddings created:",
        len(chunks_with_embeddings)
    )

    if len(chunks_with_embeddings) > 0:

        vector_size = len(
            chunks_with_embeddings[0]["embedding"]
        )

        print("Embedding vector size:", vector_size)

    return chunks_with_embeddings