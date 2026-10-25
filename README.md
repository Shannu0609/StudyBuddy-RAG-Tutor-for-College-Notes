# PDF RAG Chatbot

A Python-based Retrieval-Augmented Generation (RAG) project that lets users ask questions about information stored in PDF documents.

## About the Project

Reading and searching lengthy PDF documents can be time-consuming. This project explores how Generative AI can help users retrieve relevant information and generate answers to questions about their documents.

The application loads PDF files, splits their text into smaller chunks, creates embeddings, and stores them in a local Chroma vector database. When a user asks a question, the application retrieves relevant content and passes it to an OpenAI language model to generate an answer.

## Technologies Used

- **Python** — application development
- **LangChain** — document processing and retrieval chains
- **Hugging Face Embeddings** — text embedding generation
- **ChromaDB** — local vector storage and similarity search
- **OpenAI GPT-4o mini** — answer generation
- **python-dotenv** — environment variable management

## How It Works

1. **Document Loading:** Load PDF documents from the `docs_dir/` directory.
2. **Text Splitting:** Split extracted text into chunks of 2,000 characters with 500 characters of overlap.
3. **Embedding Generation:** Convert document chunks into numerical embeddings using Hugging Face embeddings.
4. **Vector Storage:** Store the embeddings in ChromaDB.
5. **Similarity Search:** Retrieve the three most relevant chunks for a user's question.
6. **Answer Generation:** Use OpenAI GPT-4o mini and LangChain's `RetrievalQA` chain to generate an answer based on the retrieved content.
7. **Source Display:** Print the generated answer and source document paths in the terminal.

## Project Structure

```text
pdf-rag-bot/
├── docs_dir/
│   ├── 12. Ecosystem.pdf
│   └── 6. Evolution.pdf
├── ingestion.py
├── retrievel.py
├── installationProcess.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

The `vector_db/` directory is generated locally when document ingestion is run and is excluded from Git.

## Getting Started

### Prerequisites

- Python compatible with the project dependencies
- An OpenAI API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/venkataashok234/pdf-rag-bot.git
cd pdf-rag-bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your own API key. Never commit `.env` or share your API key publicly.

### 5. Ingest the PDF documents

Run:

```bash
python ingestion.py
```

This processes the PDF files and creates the local Chroma vector database.

### 6. Ask questions

After ingestion completes, run:

```bash
python retrievel.py
```

Enter a question related to the documents when prompted. The application prints the answer and the source document paths.

## Current Features

- PDF document loading
- Text chunking with overlap
- Hugging Face embedding generation
- Persistent local Chroma vector database
- Similarity-based document retrieval
- LLM-powered question answering
- Source document path display

## Learning Outcomes

This project provides hands-on practice with:

- Retrieval-Augmented Generation (RAG)
- Document ingestion and text splitting
- Embeddings and vector databases
- Similarity search and retrieval
- LangChain question-answering chains
- OpenAI API integration
- Python environments and dependency management
- Git and GitHub basics

## Future Improvements

- Build a user-friendly chat interface.
- Improve retrieval relevance and answer quality.
- Evaluate answers against the source documents.
- Add stronger error handling and logging.

## Author

Built as a hands-on project to learn and practise Generative AI application development.
