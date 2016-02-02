from flask import Flask, jsonfify
from flask_security import auth_token_required

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()