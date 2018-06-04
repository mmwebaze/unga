#!flask/bin/python
from flask import Flask, jsonify, request as req
from models import models
from faker import Faker
import uuid

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
@app.route('/unga/api/v1.0/adverts/<advert_uuid>', methods=['GET'])
def get_advert(advert_uuid):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    advert = db.adverts.find({"id": advert_uuid})

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
    fake = Faker()
    adverts = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga

    for i in range(0, 5):
        advert = models.Advert(uuid.uuid4(), fake.text())
        db.adverts.insert(advert.serialize())
        adverts.append(advert.serialize())

    mongoConnect.getClient().close()
    return jsonify(adverts)

if __name__ == '__main__':
    app.run(debug=True)