import os
from web3 import Web3

from blockchain.EvmAbstract import EvmAbstract
from docker_helper.Dockerabstract import Dockerabstract


class FantomController(Dockerabstract, EvmAbstract):
    DOCKER_TAG = "fantom_lachesis"
    DOCKER_PORTS = {3001: 3001, 8546: 8546, 5050: 5050}
    DOCKERFILE_DIR = "/Dockerfiles/Fantom/"
    URL_TESTNET = "http://localhost"
    URL_MAINNET = "https://rpcapi.fantom.network"

    def __init__(self, mainnet=False):
        if mainnet:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_MAINNET))
        else:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_TESTNET + ":" + str(3001)))
        super().__init__()
