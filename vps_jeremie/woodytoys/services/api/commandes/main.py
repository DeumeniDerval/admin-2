import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import woody

import redis

app = Flask('my_api')
cors = CORS(app)

redis_broker = redis.Redis(host='redis', port=6379, decode_responses = True)


@app.get('/api/ping')
def ping():
    return 'ping'


# ### 3. Order Service
@app.route('/api/orders/do', methods=['GET'])
def create_order():
    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    # order = request.get_json()
    product = request.args.get('order')
    order_id = str(uuid.uuid4())

    redis_broker.publish("order", json.dumps({order_id:order_id,order:order}))

    return f"Your process {order_id} has been created with this product : {product}"


@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)

    return f'order "{order_id}": {status}'


if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
