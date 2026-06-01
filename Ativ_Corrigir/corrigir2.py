import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
pasta = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "exercicio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Aluno(db.Model):
  
    __tablename__ = "alunos"


    id = db.Column(db.Integer, primary_key=True)


    nome = db.Column(db.String(100), nullable=False)

 
    email = db.Column(db.String(120), nullable=False)


with app.app_context():
   
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        print("Tabelas:", db.metadata.tables.keys())
        aluno_teste = Aluno(nome="Teste", email="teste@mail.com")
        db.session.add(aluno_teste)
        db.session.commit()
        print("Aluno inserido:", aluno_teste)
