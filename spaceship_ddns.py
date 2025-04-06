"""
Update the @ DDNS record of a domain registered with spaceship
(https://www.spaceship.com/). You can get the API key and secret from spaceship's
website.
"""

import argparse
import datetime
import os

import requests

ENDPOINT = "https://spaceship.dev/api/v1/dns/records"


def get_env_var(variable_name: str):
    domain = os.getenv(variable_name)

    if domain is None:
        raise ValueError(
            f"Please provide a domain or set {variable_name} "
            "environment variable"
        )

    return domain


def parse_args():
    parsers = argparse.ArgumentParser(description=__doc__)
    parsers.add_argument(
        "-d", "--domain",
        type=str,
        help="Domain to update",
        required=False,
    )
    parsers.add_argument(
        "-k", "--api-key",
        type=str,
        help="API key",
        required=False,
    )
    parsers.add_argument(
        "-s", "--api-secret",
        type=str,
        help="API secret",
        required=False,
    )
    args = parsers.parse_args()

    domain: str | None = args.domain
    if domain is None:
        domain = get_env_var("SPACESHIP_DDNS_DOMAIN")

    api_key: str | None = args.api_key
    if api_key is None:
        api_key = get_env_var("SPACESHIP_DDNS_API_KEY")

    api_secret: str | None = args.api_secret
    if api_secret is None:
        api_secret = get_env_var("SPACESHIP_DDNS_API_SECRET")

    return domain, api_key, api_secret


def main():
    domain, api_key, api_secret = parse_args()

    url = f"{ENDPOINT}/{domain}"
    address = requests.get('https://api.ipify.org').content.decode('utf8')

    payload = {
        "force": True,
        "items": [
            {
                "type": "A",
                "name": "@",
                "address": address,
                "ttl": 1800,
            },
        ],
    }
    headers = {
        "X-API-Key": api_key,
        "X-API-Secret": api_secret,
        "content-type": "application/json",
    }
    response = requests.put(url, json=payload, headers=headers)

    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    response_text = response.content.decode('utf8')
    print(f"(UTC) {date} HTTP {response.status_code} {response_text}")


if __name__ == "__main__":
    main()
