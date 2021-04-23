from web3 import Web3

from blockchain.EvmAbstract import EvmAbstract
from docker_helper.Dockerabstract import Dockerabstract


class OKExController(Dockerabstract, EvmAbstract):
    URL_MAINNET = "https://exchain.okexcn.com"
    URL_TESTNET = "http://18.167.77.79:26659"
    CHAIN_ID = 65

    def __init__(self, mainnet=False):
        if mainnet:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_MAINNET))
        else:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_TESTNET))
        super().__init__()
