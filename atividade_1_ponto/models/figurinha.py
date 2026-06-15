from . import db
from .base import ModeloBase


class Figurinha(ModeloBase):
    __tablename__ = "figurinhas"

    numero = db.Column(db.Integer, nullable=False)
    nome_jogador = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(80), nullable=False)

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()
