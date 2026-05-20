from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():

     nome = "Sofia"
     idade = 17

     usuario = {
        "nome": "Ana",
        "email": "ana@email.com"
     }

     alunos = ["Ana", "Carlos", "Julia", "Pedro"]

     nota = 8

     return render_template(
"index.html",
nome=nome,
idade=idade,
usuario=usuario,
alunos=alunos,
nota=nota
)

if __name__ == "__main__":
    app.run(debug=True) 