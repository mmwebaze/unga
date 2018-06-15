#!flask/bin/python
from flask import Flask, jsonify, request
from models import advert as ad, user as u, product as prod
from flask_cors import CORS
from faker import Faker
from security import basicauthentication as bs
from flask import make_response
from database import mongodb
from util import util as ut
from dummy import data
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from functools import wraps



app = Flask(__name__)

app.config.from_pyfile('config.py')

CORS(app, resources={r"/unga/api/*": {"origins": "*"}})

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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:

            return jsonify({'Message' : 'Token is missing'}), 401

        try:
            validate_token = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message' : 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/unga/api/resources')
@auth.login_required
def login():
    token = jwt.encode({'user': request.authorization.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
    print(request.authorization.username)

    #user = models.User('Michael', 'Mwebaze', 'mail@example.com')
    return jsonify({"token": token.decode('UTF-8')})

@app.route('/unga/api/v1.0/user', methods=['POST'])
def add_user():
    #Need to check password_1 == password_2

    user = u.User(request.json['fname'], request.json['lname'], request.json['email'],
                       generate_password_hash(request.json['password_1']))

    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    db.users.insert(user.serialize())
    mongoConnect.getClient().close()

    return jsonify({"user": "User with uid "+user.getUid()+" created"})

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
@app.route('/unga/api/v1.0/products', methods=['GET'])
@token_required
def get_products():
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    products = db.products.find()
    mongoConnect.getClient().close()

    for product in products:
        output.append({'id': product['_id'], 'type': product['type'], 'description': product['description'],
                    'pictures': product['pictures'], 'created': ut.timeToStr(product['created']),'published' : product['published']})
    return jsonify(output)

@app.route('/unga/api/v1.0/products/<product_id>', methods=['GET'])
def get_product(product_id):
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    product = db.products.find_one({"_id": product_id})
    mongoConnect.getClient().close()

    return jsonify({'id': product['_id'], 'type': product['type'], 'description': product['description'],
                    'pictures': product['pictures'], 'created': ut.timeToStr(product['created']),'published' : product['published']})

@app.route('/unga/api/v1.0/category/<category_id>', methods=['GET'])
def get_products_by_category(category_id):
    output = []
    print(category_id)
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    products = db.products.find({"type": category_id})
    mongoConnect.getClient().close()


    for product in products:
        output.append({'id': product['_id'], 'type': product['type'], 'description': product['description'],
                        'pictures': product['pictures'], 'created': ut.timeToStr(product['created']),'published' : product['published']})
    return jsonify(output)

#advert routes endpoint
@app.route('/unga/api/v1.0/adverts/<advert_uuid>', methods=['GET'])
def get_advert(advert_uuid):
    output = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    advert = db.adverts.find_one({"_id": advert_uuid})
    mongoConnect.getClient().close()

    return jsonify({'id': advert['_id'], 'message': advert['message'], 'created': ut.timeToStr(advert['created']),'published': advert['published']})

@app.route('/unga/api/v1.0/adverts', methods=['GET', 'OPTIONS'])
#@crossdomain(origin='*')
def get_adverts():
    adverts = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga
    ads = db.adverts.find()
    mongoConnect.getClient().close()

    for ad in ads:
        adverts.append({'id': ad['_id'], 'message': ad['message'], 'created': ut.timeToStr(ad['created']),'published': ad['published']})
    return jsonify(adverts)

#dummy data generation endpoint
@app.route('/unga/api/v1.0/dummy', methods=['GET'])
def create_dummy_data():
    fake = Faker()
    dummy = []
    mongoConnect = mongodb.MongoDb()
    db = mongoConnect.getClient().unga

    for i in range(0, 5):
        advert = ad.Advert(fake.text())
        db.adverts.insert(advert.serialize())
        dummy.append(advert.serialize())

        user = u.User(fake.name(), data.dummyPasswords[i], fake.email(), generate_password_hash(data.dummyPasswords[i]))
        db.users.insert(user.serialize())
        dummy.append(user.serialize())

        product = prod.Product(data.dummyRentalTypes[i], fake.text())
        db.products.insert(product.serialize())
        dummy.append(product.serialize())

    mongoConnect.getClient().close()
    return jsonify(dummy)

if __name__ == '__main__':
    app.run()