import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_SERVICE_URL = "http://localhost:5001" 

orders = {}

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data.get('product_id')
    
    # Check if the product exists in the Product Service
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    
    if product_response.status_code == 200:
        product_data = product_response.json()
        order_id = len(orders) + 1  # In a real application, use a unique ID generation method.
        order = {
            "id": order_id,
            "product_id": product_id,
            "product_name": product_data['name'],
            "product_price": product_data['price'],
        }
        orders[order_id] = order
        return jsonify({"message": "Order created", "order": order}), 201
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = orders.get(order_id)
    if order:
        product_id = data.get('product_id', order['product_id'])
        
        # Fetch product details from the Product Service
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        
        if product_response.status_code == 200:
            product_data = product_response.json()
            order['product_id'] = product_id
            order['product_name'] = product_data['name']
            order['product_price'] = product_data['price']
            return jsonify({"message": "Order updated", "order": order})
        else:
            return jsonify({"error": "Product not found"}), 404
    else:
        return jsonify({"error": "Order not found"}), 404


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = orders.pop(order_id, None)
    if order:
        return jsonify({"message": "Order canceled", "order": order})
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(port=5002)



#http POST http://localhost:5002/orders product_id:=2
#http GET http://localhost:5002/orders/1
#http PUT http://localhost:5002/orders/1 product_id:=3
#http DELETE http://localhost:5002/orders/1

