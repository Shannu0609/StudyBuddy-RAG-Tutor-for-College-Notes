from pathlib import Path 
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA
load_dotenv()

llm = ChatOpenAI(model ="gpt-4o-mini", temperature =0)

PROJECT_DIR = Path(__file__).parent
VECTOR_DB_DIR = PROJECT_DIR/"vector_db"
COLLECTION_NAME = "document_collection"

def load_vector_store():
    vector_store = Chroma(
        collection_name = COLLECTION_NAME,
        persist_directory = str(VECTOR_DB_DIR),
        embedding_function = HuggingFaceEmbeddings()
  
    )

    return vector_store

def retrieve_documents(question :str, k:int =3 ):
    vector_store = load_vector_store()
    results = vector_store.similarity_search(
        query = question,
        k=k,
    )
    return results

def create_qa_chain():
    vector_store = load_vector_store()

    # Check how many chunks are stored in Chroma
    print("Stored chunks:", vector_store._collection.count())

    retriever = vector_store.as_retriever(
        search_kwargs={"k":3}
    )


    qa_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = 'stuff',
        retriever = retriever,
        return_source_documents = True,
    )
    return qa_chain

if __name__ == "__main__":
    qa_chain = create_qa_chain()

    question = input("Hi! ask any question from the documents topic")

    response = qa_chain.invoke({"query": question})
    

    print("\nAnswer:")
    print(response["result"])

    print("\nSource documents:")
    for document in response["source_documents"]:
        print(document.metadata.get("source", "Unknown source"))


