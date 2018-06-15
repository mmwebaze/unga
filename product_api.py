from app import app
from database import mongodb
from flask import jsonify
from util import util as ut
from decorators import token_required

#Products endpoints
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