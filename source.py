import json
import random
import time

from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')


@app.route('/users')
def users():
    with open(app.config['USERS_SOURCE']) as fp:
        users_db = json.load(fp)
    random.shuffle(users_db)
    time.sleep(random.randint(0, 3))
    return jsonify(users_db)


if __name__ == '__main__':
    app.run()
