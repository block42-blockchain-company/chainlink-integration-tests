from definitions import ROOT_DIR
from docker_helper.Dockerabstract import Dockerabstract
import requests
import json


class ChainlinkController(Dockerabstract):
    DOCKER_TAG = 'smartcontract/chainlink:0.9.10'
    DOCKER_ENV = {
        "ETH_CHAIN_ID": 4003,
        "LINK_CONTRACT_ADDRESS": "{link_address}",
        "ETH_URL": "wss://wsapi.fantom.network",
        "DATABASE_URL": "postgresql://postgres:postgres@chainlink_postgres:5432/chainlink?sslmode=disable",
        "DATABASE_TIMEOUT": 0,
        "SECURE_COOKIES": "false",
        "ROOT": "/chainlink",
        "MIN_OUTGOING_CONFIRMATIONS": 2,
        "CHAINLINK_TLS_PORT": 0,
        "GAS_UPDATER_ENABLED": "true",
        "ALLOW_ORIGINS": "*",
        "FEATURE_EXTERNAL_INITIATORS": "true",
        "LOG_LEVEL": "debug",
        "CHAINLINK_DEV": "true"
    }
    DOCKER_PORTS = {6688: 6688}
    DOCKER_COMMAND = "local n -p /chainlink/.password -a /chainlink/.api"
    DOCKER_VOLUMES = [ROOT_DIR + "/Dockerfiles/chainlink/config:/chainlink"]

    def __init__(self, link_address):
        self.DOCKER_ENV["LINK_CONTRACT_ADDRESS"] = link_address
        super().__init__()

    def init_job(self, oracle_address):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "initiators": [
                {
                    "type": "runlog",
                    "params": {
                        "address": f"{oracle_address}"
                    }
                }
            ], "tasks": [
                {
                  "type": "httpget"
                },
                {
                  "type": "jsonparse"
                },
                {
                  "type": "ethbytes32"
                },
                {
                  "type": "ethtx"
                }
            ]
        }

        session = requests.Session()
        login = '{"email":"test@block42.tech", "password":"block42!"}'
        session.post('http://localhost:6688/sessions', headers=headers, data=login)
        response = session.post('http://localhost:6688/v2/specs', headers=headers, data=json.dumps(data))
        return response.json()["data"]["id"]

    def get_chainlink_address(self, index):
        headers = {
            'Content-Type': 'application/json',
        }
        session = requests.Session()
        login = '{"email":"test@block42.tech", "password":"block42!"}'
        session.post('http://localhost:6688/sessions', headers=headers, data=login)
        response = session.get('http://localhost:6688/v2/keys/eth', headers=headers)
        return response.json()["data"][index]["attributes"]["address"]