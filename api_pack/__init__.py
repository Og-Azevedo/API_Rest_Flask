from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///banco_dados.db'
database = SQLAlchemy(app)

from api_pack import routes