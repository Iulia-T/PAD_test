from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

products = {
    1: {"id": 1, "name": "Product A", "price": 10.0},
    2: {"id": 2, "name": "Product B", "price": 15.0},
    3: {"id": 3, "name": "Product C", "price": 20.0},
}

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_id = len(products) + 1
    product = {"id": product_id, "name": data['name'], "price": data['price']}
    products[product_id] = product
    return jsonify({"message": "Product created", "product": product}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = products.get(product_id)
    if product:
        product['name'] = data.get('name', product['name'])
        product['price'] = data.get('price', product['price'])
        return jsonify({"message": "Product updated", "product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products.pop(product_id, None)
    if product:
        return jsonify({"message": "Product deleted", "product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5001)



#http POST http://localhost:5001/products name="New Product" price:=25.0   
#http GET http://localhost:5001/products/1
#http DELETE http://localhost:5001/products/1
#http PUT http://localhost:5001/products/2 name="Updated Product A" price:=12.0


