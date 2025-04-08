from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from AppSecret import secrets
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


class Config:
    @staticmethod
    def getmodelPath():
        return "/teamspace/studios/this_studio/Models/RAG_model.gguf"

    @staticmethod
    def getModelType():
        return "mistral"

    @staticmethod
    def getModelConfig():
        return {
            'max_new_tokens': 500,
            'temperature': 0.2,
            'context_length': 2048,
            'gpu_layers': 0,
            'threads': -1,
        }

    @staticmethod
    def getEmbeddingsPath():
        return "BAAI/bge-large-en-v1.5"

    @staticmethod
    def getchatConfig():
        return {
            'chat_memory_length': 4,
            'number_of_retrieved_documents': 1,
        }

    @staticmethod
    def pdfTextSplitter():
        return {
            'chunk_size': 1024,
            'overlap': 50,
            'seperator': ["\n", "\n\n"]
        }

    @staticmethod
    def getChromaDB():
        return {
            'chromadbPath': "chromaDB",
            'collectionName': "pdf"
        }

    @staticmethod
    def getdb():
        return db
    
    @staticmethod
    def getbcrypt():
        return bcrypt

    @staticmethod
    def getlogin():
        return login_manager

    @staticmethod
    def getMail():
        mail = Mail()
        return mail
    
    @staticmethod
    def configureApp(app):
        app.secret_key = secrets.getSecretKey()
        user = secrets.getDBUser()
        password = secrets.getDBPassword()
        host = secrets.getDBHost()
        port = secrets.getDBport()
        dbname = secrets.getDatabaseName()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        MAIL_SERVER = 'smtp-relay.brevo.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USE_SSL = False
        MAIL_USERNAME = 'isharatextteam@gmail.com'
        MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
        MAIL_DEFAULT_SENDER = 'IsharaText Team'

        Config.getdb().init_app(app)
        Config.getbcrypt().init_app(app)
        Config.getlogin().init_app(app)
        Config.getMail().init_app(app)
        Config.getlogin().login_view = 'auth.login'







