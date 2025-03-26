from flask import Blueprint, request, jsonify, render_template
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain_community.vectorstores import Chroma
import requests
import json
from AppSecret import secrets

# Flask Blueprint
RagLearningBp = Blueprint('ragLearning', __name__)

# Constants
VECTOR_DB_PATH = "db/ISL-Vector-DB"
TEXT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PDF_PATH = "pdf/Indian-Sign-Language-230.pdf"  # Hardcoded PDF
N_DOC = 2

db = None  # Global variable for database
embeddings = None  # Global variable for embeddings

def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(model_name=TEXT_EMBEDDING_MODEL)
    return embeddings

def load_document():
    global db
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    db = Chroma.from_documents(split_docs, get_embeddings(), persist_directory=VECTOR_DB_PATH)
    return db

@RagLearningBp.route('/')
def index():
    global db
    if db is None:
        db = load_document()
    return render_template('rag.html')

@RagLearningBp.route('/ask', methods=['POST'])
def query():
    global db
    if db is None:
        db = load_document()
    
    user_input = request.get_json()['message']
    context = db.similarity_search(user_input, k=N_DOC)
    context_text = " ".join([doc.page_content for doc in context])
    user_input_with_context = f"Context: {context_text} Based on the above context, answer this in a teaching manner: {user_input}"
    
    auth = "Bearer " + secrets.getAPIKey()
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": auth,
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
            "transforms": ["middle-out"],
            "messages": [{"role": "user", "content": user_input_with_context}]
        })
    )
    
    return jsonify(response.json())
