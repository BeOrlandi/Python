"""
AtividadeSQLalchemy 2.0 — Loja de produtos tecnológicos
Complete os trechos marcados com TODO ALUNO.

Execute após corrigir: python app.py
"""

import os

from flask import Flask, redirect, render_template, request, url_for

# TODO ALUNO: importe SQLAlchemy
# from flask_sqlalchemy import ___________


app = Flask(__name__)
pasta_aula = os.path.abspath(os.path.dirname(__file__))

# TODO ALUNO: configure a URI do SQLite (arquivo loja.db nesta pasta)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta_aula, "___________")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# TODO ALUNO: crie o objeto db
# db = SQLAlchemy(app)


# --- MODEL: tabela produtos (COMPLETE A CLASSE) ---
class Produto(db.Model):
    # TODO ALUNO: nome da tabela
    __tablename__ = "___________"

    # TODO ALUNO: id (Integer, primary_key=True)
    # id = db.Column(...)

    # TODO ALUNO: nome String(120), nullable=False
    # TODO ALUNO: categoria String(60), nullable=False
    # TODO ALUNO: preco Float, nullable=False
    # TODO ALUNO: estoque Integer, nullable=False, default=0

    def __repr__(self):
        return f"<Produto {self.id} {self.nome}>"


# TODO ALUNO: criar tabelas no banco
# with app.app_context():
#     db.create_all()


def _ler_formulario():
    """Lê campos do POST — nomes devem bater com o HTML (name=)."""
    return {
        "nome": request.form.get("nome", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "preco": request.form.get("preco", "").strip(),
        "estoque": request.form.get("estoque", "").strip(),
    }


def _validar(dados):
    if not dados["nome"] or not dados["categoria"] or not dados["preco"]:
        return "Preencha nome, categoria e preço."
    try:
        preco = float(dados["preco"].replace(",", "."))
        estoque = int(dados["estoque"] or 0)
    except ValueError:
        return "Preço ou estoque inválido."
    if preco < 0 or estoque < 0:
        return "Preço e estoque não podem ser negativos."
    return None


# --- READ ---
@app.route("/")
def index():
    # TODO ALUNO: busque todos os produtos ordenados por nome
    # produtos = Produto.query.order_by(Produto.nome).all()
    produtos = []
    return render_template("lista.html", produtos=produtos)


# --- CREATE ---
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        dados = _ler_formulario()
        erro = _validar(dados)
        if erro:
            return render_template(
                "formulario.html",
                titulo="Cadastrar produto",
                erro=erro,
                **dados,
            )
        produto = Produto(
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=float(dados["preco"].replace(",", ".")),
            estoque=int(dados["estoque"] or 0),
        )
        # TODO ALUNO: add + commit
        # db.session._________(produto)
        # db.session.___________()
        return redirect(url_for("index"))

    return render_template("formulario.html", titulo="Cadastrar produto")


# --- UPDATE ---
@app.route("/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
    # TODO ALUNO: buscar produto pelo id
    # produto = db.session.get(Produto, produto_id)
    produto = None

    if not produto:
        return redirect(url_for("index"))

    if request.method == "POST":
        dados = _ler_formulario()
        erro = _validar(dados)
        if erro:
            return render_template(
                "formulario.html",
                titulo="Editar produto",
                erro=erro,
                produto_id=produto.id,
                **dados,
            )
        produto.nome = dados["nome"]
        produto.categoria = dados["categoria"]
        produto.preco = float(dados["preco"].replace(",", "."))
        produto.estoque = int(dados["estoque"] or 0)
        # TODO ALUNO: commit
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar produto",
        nome=produto.nome,
        categoria=produto.categoria,
        preco=produto.preco,
        estoque=produto.estoque,
        produto_id=produto.id,
    )


# --- DELETE ---
@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    # TODO ALUNO: buscar, delete e commit
    produto = None
    if produto:
        pass
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
