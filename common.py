from http import HTTPStatus
import requests

IPIFY = "https://api.ipify.org?format=json"
POSTMAN = "https://postman-echo.com/post"


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
