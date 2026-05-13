from flask import Flask

app = Flask(__name__)


@app.route("/")
def curriculo():
    return """

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Currículo</title>
    <style>
        body { 
            font-family: Arial;
            margin: 40px;
            background-color: #f4f4f4;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
        }

        h1 {
            color: #333;
        }

        h2 {
            color: #555;
            border-bottom: 1px solid #ccc;
        }

        ul {
            list-style-type: square;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>dados.nome </h1>

    <p><strong>Telefone:</strong>  dados.telefone </p>
    <p><strong>Email:</strong>  dados.email </p>

    <h2>Escolas</h2>
    <ul>
        {% for escola in dados.escolas %}
            <li>Sesi</li>
    </ul>

    <h2>Experiência Profissional</h2>
    <ul>
         experiencias 
            <li>
                <strong> Estagiario </strong> -  Cotemig 
                ( 2 anos )
            </li>
    </ul>

    <h2>Cursos</h2>
    <ul>
        cursos 
            <li> curso </li>
        
    </ul>

    <h2>Idiomas</h2>
    <p><strong>Inglês:</strong> Expert p>
    <p><strong>Espanhol:</strong> intermediario</p>
</div>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
