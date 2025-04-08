from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from blueprints.auth import authBp
from blueprints.home import homeBp
from blueprints.dictionary import dictionaryBp
from blueprints.textToSign import TTSBp
from blueprints.ragLearning import RagLearningBp
from blueprints.meetup import meetupBp
from blueprints.join import joinBp
app = Flask(__name__)

Config.configureApp(app)

# Register Blueprints
# app.register_blueprint(authBp, url_prefix="/auth")
app.register_blueprint(homeBp, url_prefix="/")
app.register_blueprint(dictionaryBp, url_prefix="/dictionary")
app.register_blueprint(TTSBp, url_prefix="/textToSign")
app.register_blueprint(RagLearningBp, url_prefix="/ragLearning")
app.register_blueprint(meetupBp, url_prefix="/meetup")
app.register_blueprint(joinBp, url_prefix="/join")


# Initialize DB
with app.app_context():
    Config.getdb().create_all()




if __name__ == "__main__":
    app.run(debug=True, port=8000)
