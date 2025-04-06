

# Spaceship DDNS

This is a single (dockerized) Python 3 script to update the IP of a domain registered with [Spaceship](https://www.spaceship.com/).


## Usage


### CLI interface

To use the CLI interface you first have to install the dependencies as follows

```bash
pip install -r requirements.txt
```

Then, you can either run the script using command line arguments.

```bash
python3 ./spaceship_ddns.py -d domain-name -k api-key -s api-secret
# Help available with `python3 -h ./spaceship_ddns.py`
```

Alternatively, you can set up the `SPACESHIP_DDNS_DOMAIN`, `SPACESHIP_DDNS_API_KEY` and `SPACESHIP_DDNS_API_SECRET` environment variables and run the script without arguments.


### Docker compose

Create a new empty .env file with the following environment variables:

```
SPACESHIP_DDNS_DOMAIN=YourDomainHere
SPACESHIP_DDNS_API_KEY=YourApiKeyHere
SPACESHIP_DDNS_API_SECRET=YourApiSecretHere
```

Then you can run the container with a single command.

```bash
docker compose up
```


## References

  - [API docs](https://docs.spaceship.dev/#tag/DNS-records/operation/saveRecords)
