from flask import *
from Tager import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




def noUnauthorized():
    data = {
        "name": "tags-classification",
        "method": "GET",
        "code": "401",
        "error": "Unauthorized access"
    }
    return app.response_class(
        response=json.dumps(data),
        status=401,
        mimetype='application/json'
    )
def respons(tags):
    data = {
        "name": "tags-classification",
        "method": "POST",
        "code": "200",
        "tags": tags

    }
    return app.response_class(
        response=json.dumps(data),
        status=401,
        mimetype='application/json'
    )

@app.route('/')
def index():
    return "test"

@app.route("/api/tager", methods=['GET', 'POST'])
def api_tager():
    print(request.method)

    # if request.method == "GET":
    #     return noUnauthorized()
    tager = Tager(models_path='models/', encoders_path='encoders/')
    txt = request.json['Body'] + ' ' + request.json['Title']
    tags = tager.pridict(txt)
    print(tags)
    print(request.json)

    return  respons(tags[0])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
if __name__ == '__main__':
    app.run(debug=True)
