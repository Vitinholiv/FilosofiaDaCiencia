from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def indexe():
    return "Página inicial"

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)