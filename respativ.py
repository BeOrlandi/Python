from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('decorator') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def decoarator():
    return 'Decorator é uma função que modifica ou estende o comportamento de outra função, método ou classe sem alterar seu código-fonte original. Ele serve para mapear a funçao abaixo da rota' # Isso é o que será retornado quando a rota '/' for acessada

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento
