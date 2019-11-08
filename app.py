import concurrent.futures
from functools import partial
from json import JSONDecodeError

import requests
from flask import Flask, jsonify
from requests import RequestException

app = Flask(__name__)
fetch = partial(requests.get, timeout=2)


def fetch_users():
    urls = [
        'http://127.0.0.1:5001/users',
        'http://127.0.0.1:5002/users',
        'http://127.0.0.1:5003/users',
    ]
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = (executor.submit(fetch, url) for url in urls)
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result().json()
            except RequestException:
                result = []
            except JSONDecodeError:
                result = []
            results.extend(result)
    return results


@app.route('/')
def users():
    fetched_users = fetch_users()
    results = sorted(fetched_users, key=lambda v: v['id'])
    return jsonify(results)


if __name__ == '__main__':
    app.run()
