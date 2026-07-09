from src.config import DOCUMENTS_FOLDER


def load_documents():

    documents = []

    text_files = sorted(DOCUMENTS_FOLDER.glob("*.txt"))

    if len(text_files) == 0:
        raise FileNotFoundError(
            "No text files were found in the documents folder."
        )

    for file_path in text_files:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().strip()

        if text != "":
            document = {
                "file_name": file_path.name,
                "text": text
            }

            documents.append(document)

    print("Total documents loaded:", len(documents))

    return documents


def show_document_samples(documents):

    print("\nDocument Samples\n")

    for document in documents:

        print("File Name:", document["file_name"])

        print("Preview:", document["text"][:200])

        print("-" * 70)