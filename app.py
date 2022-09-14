import json
from random import randint

from flask import Flask, request, jsonify
from opentelemetry import trace, metrics
from opentelemetry.trace import SpanKind

from common import get_ip, postman_echo

# Acquire tracer
tracer = trace.get_tracer(__name__)


app = Flask(__name__)


@app.route('/')
def root():
    with tracer.start_as_current_span("do_thing") as current_span:
        current_span.add_event("Get IP")
        ip_address = get_ip()
        current_span.add_event("Call Postman Echo Service")
        echo = postman_echo(server_ip=ip_address,
                            user_agent=request.headers['user-agent'])
        return jsonify(echo)


if __name__ == "__main__":
    app.run('0.0.0.0')
