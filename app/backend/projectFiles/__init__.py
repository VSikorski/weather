import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

#setup the application and setup Cross-origin Resource Sharing
app = Flask(__name__)
CORS(app)

#configurations
app.config["SECRET_KEY"] = "mysecretkey"

#search base directory
basedir = os.path.abspath(os.path.dirname(__file__))

#setup the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

Migrate(app, db)
