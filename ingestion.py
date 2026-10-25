
from pathlib import Path
from langchain_community.document_loaders import UnstructuredFileLoader , DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

import nltk
nltk.download("punkt_tab")

# python -m pip install unstructured-inference

# Folder containing our PDF documents
DOCS_DIR = Path(__file__).parent/"docs_dir"

def load_documents():
    "loading the documents"
    loader = DirectoryLoader(
        path = str(DOCS_DIR),
        glob = "*.pdf",
        loader_cls = UnstructuredFileLoader,
        show_progress = True,
    )

    documents = loader.load()
    return documents


if __name__ == "__main__":
    documents = load_documents()
    text_splitter = CharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 500,
    )

    text_chunks = text_splitter.split_documents(documents)
    # Store the vector database inside our project folder
    VECTOR_DB_DIR = Path(__file__).parent / "vector_db"

    # Name of the Chroma collection
    COLLECTION_NAME = "document_collection"
    vector_store = Chroma.from_documents(
        documents = text_chunks,
        embeddings = HuggingFaceEmbeddings(),
        persist_directory = str(VECTOR_DB_DIR),
        collection_name = COLLECTION_NAME,
    )

