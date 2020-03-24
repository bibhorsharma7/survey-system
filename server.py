# Server

from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "aabc0f09"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

