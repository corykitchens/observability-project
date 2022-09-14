import json
from random import randint
from flask import Flask, request, jsonify

from common import get_ip, postman_echo

app = Flask(__name__)


@app.route('/')
def root():
    ip_address = get_ip()
    echo = postman_echo(server_ip=ip_address,
                        user_agent=request.headers['user-agent'])
    return jsonify(echo)


if __name__ == "__main__":
    app.run('0.0.0.0')
