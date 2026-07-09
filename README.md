# Assignment 2: Improve and Evaluate a RAG System

## Project Overview

This project improves and evaluates the Retrieval-Augmented Generation (RAG) system developed in Assignment 1.

The system loads text documents, divides them into smaller chunks, generates embeddings using the OpenAI API, stores the vectors in a local Qdrant database, retrieves relevant chunks based on a user question, and generates a final answer using a language model.

The project also investigates how chunk size, chunk overlap, Top-K retrieval, and prompt design affect retrieval quality and final-answer accuracy.

---

## Key Features

- Loads ten text documents from different topics
- Supports configurable chunk size and chunk overlap
- Generates text embeddings using OpenAI
- Stores embeddings and metadata in Qdrant Local
- Retrieves relevant chunks using cosine similarity
- Displays similarity scores, source files, and chunk numbers
- Compares three chunk-size configurations
- Compares Top-1, Top-3, and Top-5 retrieval
- Evaluates ten easy, medium, and difficult questions
- Tests questions whose answers are not available in the documents
- Uses a strict prompt to reduce hallucination
- Detects the embedding vector size dynamically
- Reuses existing Qdrant collections to reduce unnecessary API costs

---

## Technology Stack

- Python
- Jupyter Notebook
- OpenAI API
- OpenAI `text-embedding-3-small`
- OpenAI `gpt-4o-mini`
- Qdrant Local Vector Database
- pandas
- python-dotenv
- PyCharm

---

## RAG Workflow

```text
Documents
    ↓
Document Loading
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Qdrant Vector Database
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Retrieved Chunks
    ↓
Prompt Creation
    ↓
Language Model
    ↓
Final Answer
```

---

## Project Structure

```text
rag-assignment-2/
│
├── data/
│   └── documents/
│       ├── artificial_intelligence.txt
│       ├── data_science.txt
│       ├── football.txt
│       ├── health.txt
│       ├── history.txt
│       ├── machine_learning.txt
│       ├── programming.txt
│       ├── python.txt
│       ├── space.txt
│       └── travel.txt
│
├── notebooks/
│   └── assignment2.ipynb
│
├── src/
│   ├── __init__.py
│   ├── chunking.py
│   ├── config.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── ingestion.py
│   ├── prompt.py
│   ├── rag_pipeline.py
│   ├── retrieval.py
│   └── vector_store.py
│
├── screenshots/
├── qdrant_storage/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Module Description

| File | Purpose |
|---|---|
| `ingestion.py` | Loads all text documents from the documents folder |
| `chunking.py` | Divides documents into overlapping text chunks |
| `embeddings.py` | Generates embeddings using the OpenAI Embedding API |
| `vector_store.py` | Creates local Qdrant collections and stores vectors |
| `retrieval.py` | Retrieves the most similar document chunks |
| `prompt.py` | Creates weak and strict prompts |
| `generation.py` | Generates the final answer using the OpenAI language model |
| `rag_pipeline.py` | Connects document loading, chunking, embedding, and storage |
| `config.py` | Loads API keys, model names, and project paths |
| `assignment2.ipynb` | Demonstrates all experiments, outputs, and evaluations |

---

## Dataset

The dataset contains ten text documents covering different topics:

- Artificial Intelligence
- Python
- Machine Learning
- Data Science
- Football
- Travel
- Space Exploration
- World History
- Public Health
- Software Programming

The documents are stored inside:

```text
data/documents/
```

---

## Setup Instructions

### 1. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

---

### 2. Install the Required Packages

Run:

```bash
python -m pip install -r requirements.txt
```

The required packages include:

```text
openai
qdrant-client
python-dotenv
pandas
jupyter
ipykernel
```

---

### 3. Configure Environment Variables

Copy `.env.example` and rename the copied file to:

```text
.env
```

The `.env.example` file contains:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini

```

Add the real OpenAI API key only inside the private `.env` file:

```env
OPENAI_API_KEY=your_real_openai_api_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
```

---

## How to Run the Project

Start Jupyter Notebook from the project root:

```bash
jupyter notebook notebooks
```

Open:

```text
notebooks/assignment2.ipynb
```

Run all notebook cells from top to bottom.

During the first run, document embeddings and Qdrant collections will be created.

During later runs, complete existing collections will be reused, and unnecessary document embedding calls will be skipped.

---

## Experiment 1: Chunk-Size Comparison

Three chunk configurations were tested using the same question.

| Experiment | Chunk Size | Chunk Overlap | Total Chunks |
|---|---:|---:|---:|
| A | 300 | 50 | 161 |
| B | 500 | 50 | 103 |
| C | 800 | 100 | 67 |

### Observations

**Experiment A — 300/50**

- Produced the highest number of chunks
- Retrieved focused information
- Sometimes separated related information into different chunks

**Experiment B — 500/50**

- Produced a moderate number of chunks
- Retrieved focused and sufficiently complete information
- Provided a good balance between context and retrieval precision

**Experiment C — 800/100**

- Produced the lowest number of chunks
- Provided more surrounding context
- Sometimes included additional information that was not directly required

### Selected Configuration

```text
Chunk Size: 500
Chunk Overlap: 50
```

The 500/50 configuration was selected because it provided the best overall balance between focused information and sufficient context.

---

## Experiment 2: Top-K Comparison

The same question was tested using:

- Top-1
- Top-3
- Top-5

### Observations

**Top-1**

- Retrieved the single most relevant chunk
- Produced a concise answer
- Could miss supporting information for complex questions

**Top-3**

- Added useful supporting information
- Kept the retrieved context focused
- Produced clear and reliable answers

**Top-5**

- Provided more context
- Included some lower-ranked and less relevant chunks
- Increased the amount of text sent to the language model

### Selected Top-K Value

```text
Top-K: 3
```

Top-3 was selected because it provided a practical balance between sufficient context and retrieval noise.

---

## Retrieval Evaluation

The system was evaluated using ten questions with different difficulty levels:

- Easy questions
- Medium questions
- Difficult questions

For each question, the notebook displayed:

- Retrieved chunks
- Similarity scores
- Source filenames
- Chunk numbers
- Final generated answer
- Manual relevance judgment

### Evaluation Results

```text
Total Questions: 10
Correct Retrievals: 9
Correct Final Answers: 9
Retrieval Accuracy: 90%
Final Answer Accuracy: 90%
```

One difficult question about natural language processing and computer vision failed because the retrieved chunks did not contain the exact supporting information.

Although the expected source document was retrieved, the actual chunks were not sufficiently relevant. This shows that retrieving the correct file does not always mean that the correct passage was retrieved.

The strict prompt prevented the model from creating an unsupported answer.

---

## Unknown-Question Testing

The following questions were tested even though their answers were not available in the documents:

- What is Docker?
- What is Kubernetes?
- Who won the FIFA World Cup in 2022?

Qdrant still returned the closest available chunks because vector search always attempts to find the nearest stored vectors.

However, the retrieved chunks did not contain the required answers.

The strict prompt instructed the model to reply with:

```text
I don't have enough information to answer this question based on the available documents.
```

This reduced the risk of hallucination.

---

## Prompt Comparison

A weak prompt and an improved strict prompt were compared.

### Weak Prompt

The weak prompt only asked the model to use the context when answering.

It did not clearly prevent:

- Outside knowledge
- Guessing
- Unsupported information
- Inconsistent unknown-question responses

### Strict Prompt

The strict prompt instructed the model to:

- Answer only from the retrieved context
- Avoid using outside knowledge
- Avoid guessing
- Avoid inventing missing information
- Return a fixed response when the answer is unavailable

### Conclusion

The strict prompt produced more consistent and controlled answers and was selected for the final RAG pipeline.

---


## Challenges Encountered

The main challenges were:

- Understanding chunk size and chunk overlap
- Avoiding word-level chunking problems
- Managing local Qdrant storage
- Preventing repeated embedding API calls
- Detecting vector size dynamically
- Comparing Top-K values fairly
- Understanding similarity scores
- Distinguishing a relevant document from a relevant chunk
- Handling questions whose answers were unavailable
- Preventing hallucination
- Organizing code into reusable modules
- Keeping API keys secure

---

## Limitations

This project has several limitations:

- The dataset is small and was created for learning purposes
- Retrieval evaluation was performed manually
- Similarity score alone does not guarantee that a chunk contains the answer
- Only vector similarity search was used
- No hybrid keyword and vector search was implemented
- No reranking model was used
- The selected chunk size may not be best for every dataset
- Results may change if the documents or questions are modified
- Local Qdrant is suitable for this assignment but is not a production deployment

---

## Screenshots

The `screenshots/` folder contain examples of:

- Chunk samples
- Similarity-search results
- Chunk-size comparisons
- Top-K comparisons
- Evaluation tables
- Unknown-question responses

---

## Final Configuration

```text
Documents: 10
Selected Chunk Size: 500
Selected Chunk Overlap: 50
Selected Top-K: 3
Embedding Model: text-embedding-3-small
Chat Model: gpt-4o-mini
Vector Database: Qdrant Local
Retrieval Accuracy: 90%
Final Answer Accuracy: 90%
```