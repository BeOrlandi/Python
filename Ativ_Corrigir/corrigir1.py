import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

pasta = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "exercicio.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


if __name__ == "__main__":
    print("Configuração OK! Banco:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Objeto db:", db)
