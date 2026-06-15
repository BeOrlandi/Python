from . import db
from .base import ModeloBase


class OfertaTroca(ModeloBase):
    __tablename__ = "ofertas_troca"

    colecionador_id = db.Column(
        db.Integer,
        db.ForeignKey("colecionadores.id"),
        nullable=False
    )

    observacao = db.Column(db.String(255), nullable=True)

    colecionador = db.relationship(
        "Colecionador",
        back_populates="ofertas"
    )

    itens = db.relationship(
        "ItemOferta",
        back_populates="oferta",
        cascade="all, delete-orphan"
    )

    @classmethod
    def listar_com_colecionador(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()