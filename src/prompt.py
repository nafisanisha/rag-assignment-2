UNKNOWN_ANSWER = (
    "I don't have enough information to answer this question "
    "based on the available documents."
)


def create_context(retrieved_chunks):

    context_parts = []

    for chunk in retrieved_chunks:

        context_part = (
            f"Source: {chunk['file_name']}\n"
            f"Chunk Number: {chunk['chunk_number']}\n"
            f"Text: {chunk['text']}"
        )

        context_parts.append(context_part)

    context = "\n\n".join(context_parts)

    return context


def create_prompt(question, retrieved_chunks):

    context = create_context(retrieved_chunks)

    prompt = f"""
Answer only using the retrieved context below.

Rules:
1. Do not use outside knowledge.
2. Do not guess or create missing information.
3. Keep the answer clear and concise.
4. If the answer cannot be found in the context, reply exactly with:
{UNKNOWN_ANSWER}

Retrieved Context:
{context}

User Question:
{question}

Final Answer:
"""

    return prompt.strip()
def create_weak_prompt(question, retrieved_chunks):

    context = create_context(retrieved_chunks)

    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt.strip()