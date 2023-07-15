import requests


def test_healthcheck_blackbox(spawn_app):
    port = spawn_app

    endpoint = "http://127.0.0.1:" + str(port) + "/healthcheck"

    req = requests.get(endpoint)

    assert req.status_code == 200
