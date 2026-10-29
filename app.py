import os
import streamlit as st
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings
from google import genai
from google.genai import types

st.set_page_config(page_title="StudyBuddy RAG Tutor", page_icon="📚", layout="wide")
st.title("📚 StudyBuddy: College Notes RAG Tutor")

# 1. API Key retrieval
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("Missing Gemini API Key. Please add GEMINI_API_KEY to your Render Environment Variables or Streamlit secrets.")
    st.stop()

@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=api_key)

client = get_genai_client()

# 2. ChromaDB client setup
@st.cache_resource
def get_chroma_client():
    return chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))

chroma_client = get_chroma_client()

try:
    collection = chroma_client.get_or_create_collection(name="college_notes")
except Exception:
    chroma_client.delete_collection("college_notes")
    collection = chroma_client.create_collection("college_notes")

# 3. Document text extraction
def extract_text_chunks(pdf_file, chunk_size=800, overlap=100):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# 4. Embeddings using Google GenAI API
def embed_chunks(chunks):
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=chunks,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return [e.values for e in response.embeddings]

def embed_query(query_text):
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=[query_text],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return response.embeddings[0].values

# 5. Sidebar PDF ingestion
with st.sidebar:
    st.header("Upload Course Materials")
    uploaded_file = st.file_uploader("Upload College PDF Notes", type=["pdf"])
    
    if uploaded_file and st.button("Process & Index Document"):
        with st.spinner("Extracting text and indexing embeddings..."):
            chunks = extract_text_chunks(uploaded_file)
            if not chunks:
                st.warning("Could not extract readable text from this PDF.")
            else:
                batch_size = 50
                all_embeddings = []
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    all_embeddings.extend(embed_chunks(batch))

                existing_count = collection.count()
                ids = [f"chunk_{existing_count + i}" for i in range(len(chunks))]
                collection.add(
                    ids=ids,
                    embeddings=all_embeddings,
                    documents=chunks
                )
                st.success(f"Indexed {len(chunks)} chunks successfully!")

# 6. Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask a question about your uploaded notes...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if collection.count() == 0:
            response_text = "Please upload and process a PDF in the sidebar before asking questions."
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            with st.spinner("Searching notes and generating answer..."):
                query_vec = embed_query(user_query)
                results = collection.query(
                    query_embeddings=[query_vec],
                    n_results=min(4, collection.count())
                )
                retrieved_docs = results["documents"][0] if results["documents"] else []
                context = "\n\n---\n\n".join(retrieved_docs)

                rag_prompt = f"""You are StudyBuddy, an academic AI tutor for college students. 
Answer the student's question accurately using only the retrieved course notes context provided below.
If the notes do not contain sufficient information, state that clearly and provide guidance based on first principles.

Relevant Context from Notes:
{context}

Student Question:
{user_query}
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=rag_prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
