# from flask import Blueprint, request, jsonify, render_template
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI
# from langchain_community.vectorstores import Chroma
# import requests
# import json
# from AppSecret import secrets

# # Flask Blueprint
# RagLearningBp = Blueprint('ragLearning', __name__)

# # Constants
# VECTOR_DB_PATH = "db/ISL-Vector-DB"
# TEXT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# PDF_PATH = "pdf/Indian-Sign-Language-230.pdf"  # Hardcoded PDF
# N_DOC = 2

# db = None  # Global variable for database
# embeddings = None  # Global variable for embeddings

# def get_embeddings():
#     global embeddings
#     if embeddings is None:
#         embeddings = HuggingFaceEmbeddings(model_name=TEXT_EMBEDDING_MODEL)
#     return embeddings

# def load_document():
#     global db
#     loader = PyPDFLoader(PDF_PATH)
#     docs = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = text_splitter.split_documents(docs)
#     db = Chroma.from_documents(split_docs, get_embeddings(), persist_directory=VECTOR_DB_PATH)
#     return db

# @RagLearningBp.route('/')
# def index():
#     global db
#     if db is None:
#         db = load_document()
#     return render_template('rag.html')

# @RagLearningBp.route('/ask', methods=['POST'])
# def query():
#     global db
#     if db is None:
#         db = load_document()
    
#     user_input = request.get_json()['message']
#     context = db.similarity_search(user_input, k=N_DOC)
#     context_text = " ".join([doc.page_content for doc in context])
#     user_input_with_context = f"Context: {context_text} Based on the above context, answer this in a teaching manner: {user_input}"
    
#     auth = "Bearer " + secrets.getAPIKey()
#     response = requests.post(
#         url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": auth,
#             "Content-Type": "application/json"
#         },
#         data=json.dumps({
#             "model": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
#             "transforms": ["middle-out"],
#             "messages": [{"role": "user", "content": user_input_with_context}]
#         })
#     )
    
#     return jsonify(response.json())




from flask import Blueprint, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from flask import render_template
from dotenv import load_dotenv
import os

RagLearningBp = Blueprint('ragLearning', __name__)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
VECTOR_DB_PATH = "db/ISL-Vector-DB"

# Load once and reuse
loader = PyPDFLoader("pdf/Indian-Sign-Language-230.pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(pages)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
dbChroma = Chroma.from_documents(chunks, embeddings, persist_directory=VECTOR_DB_PATH)

model = ChatOpenAI(
    model="google/gemini-2.5-pro-exp-03-25:free",
    base_url="https://openrouter.ai/api/v1/",
    api_key=OPENROUTER_API_KEY
)

PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
Answer the question based on the above context: {question}.
Provide a detailed answer.
The Context is about Indian Sign Language so the response should be in a teaching manner and from context.
Don't give information not mentioned in the CONTEXT INFORMATION.
Do not say "according to the context" or "mentioned in the context" or similar.
"""


@RagLearningBp.route('/', methods=['GET'])
def chat_page():
    return render_template('rag.html')

@RagLearningBp.route('/chat', methods=['POST'])
def chat_with_isl_bot():
    data = request.get_json()
    query = data.get("question", "")

    docs_chroma = dbChroma.similarity_search(query, k=5)
    context = " ".join([doc.page_content for doc in docs_chroma])
    prompt = PROMPT_TEMPLATE.format(context=context, question=query)


    formatted_prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    

    try:
        response = model.invoke([
            {"role": "system", "content": "You are an Indian Sign Language tutor answering student questions based on the provided content."},
            {"role": "user", "content": formatted_prompt}
        ])
        return jsonify({"answer": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
