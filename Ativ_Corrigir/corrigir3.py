import os

from flask import Flask, request
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


def cadastrar_aluno(nome, email):
    """CREATE — insere um aluno no banco."""
    aluno = Aluno(nome=nome, email=email)

   
    db.session.add(aluno)


    db.session.commit()

    return aluno


if __name__ == "__main__":
    with app.app_context():
        with app.test_request_context(
            method="POST",
            data={"nome": "Maria", "email": "maria@escola.com"},
        ):
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()

            if nome and email:
                registro = cadastrar_aluno(nome, email)
                print("Cadastrado:", registro.nome, registro.email, "id=", registro.id)
            else:
                print("Dados inválidos no formulário.")

        total = Aluno.query.count()
        print("Total no banco:", total)
