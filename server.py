import flask
from flask import Flask, app, make_response

app = Flask(__name__)


@app.route("/")
def ip():
    try:
        return make_response(flask.request.remote_addr)
    except:
        return "error"


app.run("0.0.0.0", 10240, debug=False)
