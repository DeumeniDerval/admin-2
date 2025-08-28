import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import woody

import json

import threading

import redis

app = Flask('my_api')
cors = CORS(app)

redis_db = redis.Redis(host='redis', port=6379, db=0)
redis_broker = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


@app.get('/api/ping')
def ping():
    return 'ping'


# ### 2. Product Service ###
@app.route('/api/products', methods=['GET'])
def add_product():
    # product = request.json.get('product', '')
    product = request.args.get('product')
    woody.add_product(str(product))
    return str(product) or "none"


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return "not yet implemented"


@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    last_product = redis_db.get("last")
    if last_product is None:
        last_product = woody.get_last_product()  # note: it's a very slow db query
        redis_db.setex("last",60,last_product)
    return f'db: {datetime.now()} - {last_product}'


def prepare_order(order_id, order):
    status = woody.make_heavy_validation(order)
    woody.save_order(order_id,status,order)


def order_watcher():
    broker=redis_broker.pubsub()
    pubsub.subscribe('orders')
    for message in pubsub.listen():
        if message['type']=='message':
            data=json.loads(message["data"])
            prepare_order(data["order_id"],data["order"])


if __name__ == "__main__":
    thread=threading.Thread(target=order_watcher)
    thread.start()
    woody.launch_server(app, host='0.0.0.0', port=5000)
