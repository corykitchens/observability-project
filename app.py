import os
from http import HTTPStatus
import requests
from flask import Flask, request, jsonify

from telemetry import configure_tracer, configure_meter


app_name = os.getenv('APP_NAME', 'obs-app')
app_version = os.getenv('APP_VERSION', '0.0.1')

tracer = configure_tracer(app_name, app_version)
meter = configure_meter(app_name, app_version)

requests_counter = meter.create_counter(
    "number_of_requests"
)

app = Flask(__name__)


@tracer.start_as_current_span("get IP")
def get_ip():
    ipify_url = "https://api.ipify.org?format=json"
    resp = requests.get(ipify_url)
    return send_response(resp, "IPIFY")


@tracer.start_as_current_span("postman echo")
def postman_echo(server_ip, user_agent):
    postman_url = "https://postman-echo.com/post"
    resp = requests.post(
        postman_url, json={"server_ip": server_ip, "user_agent": user_agent})
    return send_response(resp, "Postman")


@tracer.start_as_current_span("send response")
def send_response(resp, endpoint):
    if resp.status_code != HTTPStatus.OK:
        print(f"#{endpoint} responded with #{resp.status_code}")
        return {}
    return resp.json()


@app.route('/healthz')
def health_check():
    with tracer.start_as_current_span("healthz") as current_span:
        return jsonify({"status": "OK"})


@app.route('/')
def root():
    requests_counter.add(1)
    with tracer.start_as_current_span("root") as current_span:
        ip_address = get_ip()
        current_span.add_event("Call Postman Echo Service")
        echo = postman_echo(server_ip=ip_address,
                            user_agent=request.headers['user-agent'])
        return jsonify(echo)


if __name__ == "__main__":
    app.run('0.0.0.0')
