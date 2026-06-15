from flask import Flask
from models import db
from controllers.figurinhas_controller import figurinhas_bp

app.register_blueprint(figurinhas_bp)

from controllers.figurinhas_controller import figurinhas_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///figurinhas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(figurinhas_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return """
    <h1>Sistema de Troca de Figurinhas</h1>
    <p><a href='/figurinhas/'>Ir para as ofertas</a></p>
    """


if __name__ == "__main__":
    app.run(debug=True)