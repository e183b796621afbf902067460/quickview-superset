import requests
import os
import typing
import logging
import time


CLICKHOUSE_PASSWORD: typing.Optional[str] = os.getenv('CLICKHOUSE_PASSWORD', None)

SUPERSET_HOST: typing.Optional[str] = os.getenv('SUPERSET_HOST', None)
SUPERSET_PORT: typing.Optional[int] = os.getenv('SUPERSET_PORT', None)
SUPERSET_USERNAME: typing.Optional[str] = os.getenv('SUPERSET_USERNAME', None)
SUPERSET_PASSWORD: typing.Optional[str] = os.getenv('SUPERSET_PASSWORD', None)

SUPERSET_URL = f'http://{SUPERSET_HOST}:{SUPERSET_PORT}'


def restart_on_exception(max_attempts, delay=0):
    """
    Decorator to restart a function if it raises a specified exception.

    :param max_attempts: Maximum number of restart attempts.
    :param delay: Delay in seconds between restart attempts.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # Replace with a specific exception if needed
                    attempts += 1
                    print(f"Exception caught: {exc}. Restarting in {delay} seconds...")
                    time.sleep(delay)
            raise Exception(f"Failed after {max_attempts} attempts.")
        return wrapper
    return decorator


@restart_on_exception(max_attempts=5, delay=5)
def login(headers: dict, payload: dict) -> str:
    response = requests.post(
        url=f'{SUPERSET_URL}/api/v1/security/login',
        headers=headers,
        json=payload
    )
    return response.json()['access_token']


@restart_on_exception(max_attempts=5, delay=5)
def assets_export(headers: dict, payload: dict, files: dict) -> requests.Response:
    response = requests.post(
        f'{SUPERSET_URL}/api/v1/assets/import',
        headers=headers,
        files=files,
        data=payload,
        verify=False
    )
    return response


# login first to get JWT token
headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
payload = {
    "password": SUPERSET_PASSWORD,
    "provider": "db",
    "refresh": True,
    "username": SUPERSET_USERNAME
}
jwt_token = login(headers=headers, payload=payload)

# export assets
files = {
    'bundle': (
        'docker-entrypoint-initdb.zip',
        open("/app/docker-entrypoint-initdb.d/docker-entrypoint-initdb.zip", "rb"),
        'application/zip'
    )
}

payload = {
    'passwords': f'{{"databases/ClickHouse.yaml": "{CLICKHOUSE_PASSWORD}"}}'
}
headers = {
    "Authorization": f"Bearer {jwt_token}",
    'Accept': 'application/json'
}
assets = assets_export(headers=headers, payload=payload, files=files)

logging.info(f'Dashboard import response: {assets.status_code}.')
