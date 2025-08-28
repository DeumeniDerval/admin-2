import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import woody

import redis

app = Flask('my_api')
cors = CORS(app)

redis_db = redis.Redis(host='redis', port=6379, db=0)


@app.get('/api/ping')
def ping():
    return 'ping'


# ### 1. Misc service ### (note: la traduction de miscellaneous est 'divers'
@app.route('/api/misc/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'


@app.route('/api/misc/heavy', methods=['GET'])
def get_heavy():
    name = request.args.get('name')
    r = redis_db.get("heavy"+name)
    if r is None:
        r = woody.make_some_heavy_computation(name)
        redis_db.set("heavy"+name,r)
    # on rajoute la date pour pas que le resultat ne soit mis en cache par le browser
    return f'{datetime.now()}: {r}'


if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)
