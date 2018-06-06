#!flask/bin/python
from flask import Flask, jsonify, request as req
from models import models
from faker import Faker
from security import basicauthentication as bs
from flask import make_response
from database import mongodb
from dummy import data
from werkzeug.security import check_password_hash


app = Flask(__name__)


basicAuth = bs.HttpBasicAuth()
auth = basicAuth.authenticate()

@auth.verify_password
def verify_password(username, password):
    if username in data.users:

        return check_password_hash(data.users.get(username), password)
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/')
@auth.login_required
def index():

    #user = models.User('Michael', 'Mwebaze', 'mail@example.com')
    return jsonify({"message": "logged in"})

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
@app.route('/unga/api/v1.0/users/<uid>', methods=['GET'])
def get_user(uid):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    users = db.users.find({"uid": uid})

    for user in users:
        output.append({'first_name': user['first_name'], 'email': user['email'], 'uid' : user['uid']})

    return jsonify(output)

@app.route('/unga/api/v1.0/users', methods=['GET'])
def get_users():
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    users = db.users.find()

    for user in users:
        output.append({
            'href': user['uri'],
            'first_name': user['first_name'],
            'email': user['email'],
            'uid' : user['uid']
        })

    return jsonify({'users': output})

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
    dummy = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga

    for i in range(0, 5):
        advert = models.Advert(fake.text())
        db.adverts.insert(advert.serialize())
        dummy.append(advert.serialize())

        user = models.User(fake.name(), fake.email(), fake.email())
        db.users.insert(user.serialize())
        dummy.append(user.serialize())



    mongoConnect.getClient().close()
    return jsonify(dummy)

if __name__ == '__main__':
    app.run(debug=True)