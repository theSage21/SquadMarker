import os
import bottle
import pymongo
from datetime import datetime


MONGO_URL = os.environ.get('MONGODB_URI')
PORT = os.environ.get("PORT")
PORT = PORT if PORT else 8000
app = bottle.Bottle()
dbname = MONGO_URL.split('/')[-1]
client = pymongo.MongoClient(MONGO_URL)
db = client[dbname]

string = 'Origin, Accept , Content-Type, X-Requested-With, X-CSRF-Token'
CORS_HEADERS = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': string
                }


@app.route('/<:re:.*>', method=['OPTIONS'])
def enableCORSGenericOptionsRoute():
    "This allows for CORS usage of the APIs"
    return 'OK'


@app.hook('after_request')
def add_cors_headers():
    "Add cors headers to all outgoing responses"
    for key, val in CORS_HEADERS.items():
        bottle.response.headers[key] = val


@app.get('/')
def home():
    with open('home.html', 'r') as fl:
        html = fl.read()
    return html


@app.post('/mark')
def mark():
    headers = bottle.headers
    doc = {"headers": headers,
           "stamp": datetime.utcnow()}
    doc.update(dict(bottle.request.json))
    db.markings.insert_one(doc)
    return 'OK'


app.run(debug=True, port=PORT, host='0.0.0.0')
