from http import HTTPStatus
import requests
from flask import request
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes


IPIFY = "https://api.ipify.org?format=json"
POSTMAN = "https://postman-echo.com/post"


def configure_meter():
    return metrics.get_meter("helloworld")


def configure_tracer(name, version):
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)

    resource = Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: name,
            ResourceAttributes.SERVICE_VERSION: version,
        }
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(name, version)


def get_ip():
    resp = requests.get(IPIFY)
    return send_response(resp, "IPIFY")


def postman_echo(server_ip, user_agent):
    resp = requests.post(
        POSTMAN, json={"server_ip": server_ip, "user_agent": user_agent})
    return send_response(resp, "Postman")


def send_response(resp, endpoint):
    if resp.status_code != HTTPStatus.OK:
        print(f"#{endpoint} responded with #{resp.status_code}")
        return {}
    return resp.json()
