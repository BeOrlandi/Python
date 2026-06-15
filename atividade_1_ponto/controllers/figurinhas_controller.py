from flask import Blueprint, redirect, render_template, request, url_for
from models import Colecionador, Figurinha, ItemOferta, OfertaTroca, db

from models import (
    Colecionador,
    Figurinha,
    ItemOferta,
    OfertaTroca,
    db
)

figurinhas_bp = Blueprint(
    "figurinhas",
    __name__,
    url_prefix="/figurinhas"
)

@figurinhas_bp.route("/")
def index():
    ofertas = OfertaTroca.listar_com_colecionador()

    return render_template(
        "figurinhas/lista_ofertas.html",
        ofertas=ofertas
    )

@figurinhas_bp.route("/oferta/cadastrar", methods=["GET", "POST"])
def cadastrar_oferta():
    colecionadores = Colecionador.listar()
    figurinhas = Figurinha.listar()

    if request.method == "POST":

        colecionador_id = request.form["colecionador_id"]
        figurinha_oferece_id = request.form["figurinha_oferece_id"]
        figurinha_deseja_id = request.form["figurinha_deseja_id"]
        observacao = request.form.get("observacao", "")

        oferta = OfertaTroca(
            colecionador_id=colecionador_id,
            observacao=observacao
        )

        db.session.add(oferta)
        db.session.flush()

        item_oferece = ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=figurinha_oferece_id,
            tipo="oferece"
        )

        item_deseja = ItemOferta(
            oferta_id=oferta.id,
            figurinha_id=figurinha_deseja_id,
            tipo="deseja"
        )

        db.session.add(item_oferece)
        db.session.add(item_deseja)

        db.session.commit()

        return redirect(url_for("figurinhas.index"))

    return render_template(
        "figurinhas/formulario_oferta.html",
        colecionadores=colecionadores,
        figurinhas=figurinhas,
    )