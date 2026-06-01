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

    def __repr__(self):
        return f"{self.id} - {self.nome}"


with app.app_context():
    db.create_all()


def listar_alunos():
    """READ — retorna todos os alunos ordenados por nome."""
    return Aluno.query.order_by(Aluno.nome).all()


def buscar_aluno(aluno_id):
    """READ — busca um aluno pelo id."""
    return db.session.get(Aluno, aluno_id)


def atualizar_aluno(aluno_id, novo_nome, novo_email):
    """UPDATE — altera nome e e-mail."""
    aluno = buscar_aluno(aluno_id)
    if not aluno:
        return False

    aluno.nome = novo_nome
    aluno.email = novo_email

  
    db.session.commit()

    return True


if __name__ == "__main__":
    with app.app_context():
        if Aluno.query.count() == 0:
            db.session.add(Aluno(nome="João", email="joao@mail.com"))
            db.session.add(Aluno(nome="Ana", email="ana@mail.com"))
            db.session.commit()

        print("--- Lista ---")
        for a in listar_alunos():
            print(a)

        print("--- Busca id=1 ---")
        print(buscar_aluno(1))

        print("--- Update id=1 ---")
        ok = atualizar_aluno(1, "João Pedro", "joao.pedro@mail.com")
        print("Atualizou?", ok, "|", buscar_aluno(1))
