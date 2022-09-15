import os

from flask import Flask, request, jsonify

from common import get_ip, postman_echo, configure_tracer, configure_meter

app_name = os.getenv('APP_NAME', 'obs-app')
app_version = os.getenv('APP_VERSION', '0.0.1')

tracer = configure_tracer(app_name, app_version)

meter = configure_meter()

requests_counter = meter.create_counter(
    "number_of_requests"
)


app = Flask(__name__)


@app.route('/healthz')
def health_check():
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
