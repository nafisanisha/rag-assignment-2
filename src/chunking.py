def split_text(text, chunk_size=500, chunk_overlap=50):

    chunks = []

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    start_position = 0
    text_length = len(text)

    while start_position < text_length:

        end_position = start_position + chunk_size

        if end_position > text_length:
            end_position = text_length

        if end_position < text_length:

            paragraph_end = text.rfind(
                "\n\n",
                start_position,
                end_position
            )

            if paragraph_end > start_position + (chunk_size // 2):
                end_position = paragraph_end

            else:
                last_space = text.rfind(
                    " ",
                    start_position,
                    end_position
                )

                if last_space > start_position:
                    end_position = last_space

        chunk_text = text[
            start_position:end_position
        ].strip()

        if chunk_text != "":
            chunks.append(chunk_text)

        if end_position >= text_length:
            break

        start_position = end_position - chunk_overlap

        next_space = text.find(
            " ",
            start_position,
            end_position
        )

        if next_space != -1:
            start_position = next_space + 1

    return chunks


def chunk_all_documents(
    documents,
    chunk_size=500,
    chunk_overlap=50
):

    all_chunks = []
    chunk_id = 0

    for document in documents:

        document_chunks = split_text(
            text=document["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk_number, chunk_text in enumerate(document_chunks):

            chunk_data = {
                "id": chunk_id,
                "file_name": document["file_name"],
                "chunk_number": chunk_number,
                "text": chunk_text
            }

            all_chunks.append(chunk_data)

            chunk_id = chunk_id + 1

    print("Chunk Size:", chunk_size)
    print("Chunk Overlap:", chunk_overlap)
    print("Total Chunks Created:", len(all_chunks))

    return all_chunks


def show_chunk_samples(chunks, number_of_samples=3):

    print("\nChunk Samples\n")

    for chunk in chunks[:number_of_samples]:

        print("File Name:", chunk["file_name"])
        print("Chunk Number:", chunk["chunk_number"])
        print("Text:")
        print(chunk["text"])
        print("-" * 70)