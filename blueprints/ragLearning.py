from flask import Blueprint, request, jsonify, render_template
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
import requests
import json
from langchain.embeddings import HuggingFaceEmbeddings
from AppSecret import secrets

# Flask Blueprint
RagLearningBp = Blueprint('ragLearning', __name__)

# Constants
VECTOR_DB_PATH = "db/ISL-Vector-DB"
TEXT_EMBEDDING_MODEL = "BAAI/bge-m3"
PDF_PATH = "Indian-Sign-Language-230.pdf"  # PDF in the same folder
N_DOC = 2

embedding_function = HuggingFaceEmbeddings(model_name=TEXT_EMBEDDING_MODEL)
def load_documents():
    loader = DirectoryLoader('pdf', glob='*.pdf')
    docs = loader.load()
   
    db = Chroma.from_documents(docs, embedding_function, persist_directory='chroma')
    return db


db = load_documents()


@RagLearningBp.route('/')
def index():
    return render_template('rag.html')

@RagLearningBp.route('/ask', methods=['POST'])
def query():
    user_input = request.get_json()['message']
    print("working on it....")

    context = db.similarity_search(user_input, k=N_DOC)

    # Combine Context and User input
    context_text = " ".join([doc.page_content for doc in context])
    
    # Optionally, split the context into smaller chunks if too long
    context_chunks = split_text(context_text)

    # Prepare user input with context
    user_input_with_context = "Context: " + "".join(context_chunks) + " " +"Based on above context answer this and responde in plain text: " + user_input
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

    print(response.json())
    return jsonify(response.json())

def split_text(text, chunk_size=1000):
    """Split the context into smaller chunks if too long."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    return text_splitter.split_text(text)
