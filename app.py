#!flask/bin/python
from flask import Flask, jsonify, request as req
from models import models
from flask_cors import CORS
from faker import Faker
from security import basicauthentication as bs
from flask import make_response
from database import mongodb
from dummy import data
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
CORS(app)

basicAuth = bs.HttpBasicAuth()
auth = basicAuth.authenticate()

@auth.verify_password
def verify_password(username, password):
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    user = db.users.find_one({'email': username})
    mongoConnect.getClient().close()

    if user:
        print(user['password'])
        if check_password_hash(user['password'], password):

            return True

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
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    user = db.users.find_one({"_id": uid})
    mongoConnect.getClient().close()

    return jsonify({'first_name': user['first_name'], 'email': user['email'], 'uid' : user['_id']})

@app.route('/unga/api/v1.0/users', methods=['GET'])
def get_users():
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    users = db.users.find()
    mongoConnect.getClient().close()

    for user in users:
        output.append({
            'href': user['uri'],
            'first_name': user['first_name'],
            'email': user['email'],
            'uid' : user['_id']
        })

    return jsonify({'users': output})

#Rentals endpoints
@app.route('/unga/api/v1.0/rentals', methods=['GET'])
def get_rentals():
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    rentals = db.rentals.find()
    mongoConnect.getClient().close()

    for rental in rentals:
        output.append({'id': rental['_id'], 'type': rental['type'], 'description': rental['description'],
                    'pictures': rental['pictures'], 'published' : rental['published']})
    return jsonify(output)

@app.route('/unga/api/v1.0/rentals/<rental_id>', methods=['GET'])
def get_rental(rental_id):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    rental = db.rentals.find_one({"_id": rental_id})
    mongoConnect.getClient().close()

    return jsonify({'id': rental['_id'], 'type': rental['type'], 'description': rental['description'],
                    'pictures': rental['pictures'], 'published' : rental['published']})

#advert routes endpoint
@app.route('/unga/api/v1.0/adverts/<advert_uuid>', methods=['GET'])
def get_advert(advert_uuid):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    advert = db.adverts.find_one({"_id": advert_uuid})
    mongoConnect.getClient().close()

    return jsonify({'id': advert['_id'], 'message': advert['message']})

@app.route('/unga/api/v1.0/adverts', methods=['GET'])
def get_adverts():
    adverts = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    ads = db.adverts.find()
    mongoConnect.getClient().close()

    for ad in ads:
        adverts.append({'id': ad['_id'], 'message': ad['message']})
    return jsonify(adverts)

#dummy data generation endpoint
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

        user = models.User(fake.name(), data.dummyPasswords[i], fake.email(), generate_password_hash(data.dummyPasswords[i]))
        db.users.insert(user.serialize())
        dummy.append(user.serialize())

        rental = models.Rental(data.dummyRentalTypes[i], fake.text())
        db.rentals.insert(rental.serialize())
        dummy.append(rental.serialize())

    mongoConnect.getClient().close()
    return jsonify(dummy)

if __name__ == '__main__':
    app.run(debug=True)