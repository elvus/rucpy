import urllib3
from flask import Flask, Response, render_template
from flask_cors import CORS
from ruc import connection
from bson.json_util import dumps

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/")
def api_root():
    db=connection()
    response=dumps(db.contribuyentes.find())
    return Response(response=response, status=200, mimetype='application/json')

@app.route("/api/<q>")
def query(q):
    db=connection()
    response=dumps(db.contribuyentes.find({
        "$or":[
                {'documento': {'$regex': q}},
                {'razonsocial': {'$regex': str(urllib3.util.parse_url(q)), "$options" :'i'}}
            ]
        })
    )
    return Response(response=response, status=200, mimetype='application/json')

if __name__=="__main__":
    app.run(host='0.0.0.0')