"""
Update the DDNS record of a domain registered with spaceship
(https://www.spaceship.com/). You can get the API key and secret from
spaceship's website.
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
            f"Please use the CLI arguments or set the {variable_name} "
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
    parsers.add_argument(
        "-N", "--name",
        type=str,
        help="Target DNS name. Use @ for domain root.",
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

    name: str | None = args.name
    if name is None:
        name = get_env_var("SPACESHIP_DDNS_NAME")

    return domain, api_key, api_secret, name


def get_dns_entries(domain: str, api_key: str, api_secret: str):
    url = f"{ENDPOINT}/{domain}?take=500&skip=0"

    headers = {
        "X-API-Key": api_key,
        "X-API-Secret": api_secret,
    }
    response = requests.get(url, headers=headers)

    response_text = response.content.decode("utf8")
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    print(f"(UTC) {date} HTTP {response.status_code} {response_text}")

    return response.json()["items"]


def delete_dns_entry(
    domain: str,
    api_key: str,
    api_secret: str,
    name: str,
    address: str,
):
    url = f"{ENDPOINT}/{domain}"

    payload = [
        {
            "type": "A",
            "name": name,
            "address": address,
        }
    ]
    headers = {
        "X-API-Key": api_key,
        "X-API-Secret": api_secret,
        "content-type": "application/json"
    }
    response = requests.delete(url, json=payload, headers=headers)

    response_text = response.content.decode("utf8")
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    print(f"(UTC) {date} HTTP {response.status_code} {response_text}")
    print(payload)


def add_dns_entry(
    domain: str,
    api_key: str,
    api_secret: str,
    name: str,
    address: str,
):
    url = f"{ENDPOINT}/{domain}"

    payload = {
        "force": True,
        "items": [
            {
                "type": "A",
                "name": name,
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

    response_text = response.content.decode("utf8")
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    print(f"(UTC) {date} HTTP {response.status_code} {response_text}")
    print(payload)


def main():
    domain, api_key, api_secret, name = parse_args()

    try:
        current_address = (
            requests
            .get("https://api.ipify.org")
            .content
            .decode("utf8")
        )
    except requests.RequestException as e:
        raise Exception("Unable to retrieve the current address") from e

    dns_entries = get_dns_entries(domain, api_key, api_secret)
    current_address_found = False
    for entry in dns_entries:
        if entry["name"] == name and entry["type"] == "A":
            if entry["address"] == current_address:
                current_address_found = True
            else:
                delete_dns_entry(
                    domain=domain,
                    api_key=api_key,
                    api_secret=api_secret,
                    name=name,
                    address=entry["address"],
                )

    if not current_address_found:
        add_dns_entry(domain, api_key, api_secret, name, current_address)


if __name__ == "__main__":
    main()
