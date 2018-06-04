#!flask/bin/python
from flask import Flask, jsonify, request as req
from models import models
import uuid, json
from bson import json_util
import requests
from database import mongodb;

app = Flask(__name__)

@app.route('/')
def index():

    user = models.User('Michael', 'Mwebaze', 'mail@example.com')
    return jsonify(user.serialize())

'''@app.route('/address')
def address():
    user = req.args.get('address')

    r = requests.get("https://nominatim.openstreetmap.org/search.php?q="+user+"&polygon_geojson")
    #return jsonify(r)
    return jsonify(
        r.text,
    r.status_code,
    r.headers['content-type'],
    )
'''
@app.route('/unga/api/v1.0/adverts/<int:advert_id>', methods=['GET'])
def get_advert(advert_id):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    advert = db.adverts.find({"id": advert_id})

    for ad in advert:
        output.append({'id': ad['id'], 'message': ad['message']})
        #abort(404)

    return jsonify(output)

@app.route('/unga/api/v1.0/adverts', methods=['GET'])
def get_adverts():
    adverts = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    ads = db.adverts.find()

    for ad in ads:
        adverts.append({'id': ad['id'], 'message': ad['message']})
    return jsonify(adverts)

@app.route('/unga/api/v1.0/dummy', methods=['GET'])
def create_dummy_data():
    adverts = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga

    for i in range(0, 5):
        advert = models.Advert(i, 'message '+str(uuid.uuid1()))
        db.adverts.insert(advert.serialize())
        adverts.append(advert.serialize())

    mongoConnect.getClient().close()
    return jsonify(adverts)

if __name__ == '__main__':
    app.run(debug=True)