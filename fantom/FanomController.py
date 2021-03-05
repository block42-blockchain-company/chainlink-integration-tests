import json
import time
from web3 import Web3
from docker_helper.Dockerabstract import Dockerabstract


class FantomController(Dockerabstract):
    DOCKER_TAG = "fantom_lachesis"
    DOCKER_PORTS = {3001: 3001, 8546: 8546, 5050: 5050}
    DOCKERFILE_DIR = "/Dockerfiles/Fantom/"
    URL = "http://localhost"
    URL_TESTNET = "https://rpcapi.fantom.network"

    def __init__(self, testnet=False):
        if testnet:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_TESTNET))
        else:
            self.w3 = Web3(Web3.HTTPProvider(self.URL + ":" + str(3001)))
        super().__init__()

    def sendFtm(self, _amount, _to):
        acct = self.w3.eth.account.privateKeyToAccount(
            "0x81ab836599c179fadf202e1ccdb61e386a3bd72f1d8fc200aa3e19422b57bf11")

        tx_hash = self.w3.eth.sendTransaction(
            {
                'to': _to,
                'from': acct.address,
                'value': _amount,
                'gas': 1728712,
                'gasPrice': self.w3.toWei('21', 'gwei')
            })
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def deploy_contract(self, abi, bytecode, *args, **kwargs) -> None:
        contract_ = self.w3.eth.contract(
            abi=abi,
            bytecode=bytecode
        )
        acct = self.w3.eth.account.privateKeyToAccount("0x81ab836599c179fadf202e1ccdb61e386a3bd72f1d8fc200aa3e19422b57bf11")
        construct_txn = contract_.constructor(*args, **kwargs).buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 210000,
            'gasPrice': self.w3.toWei('22', 'gwei')})
        signed = acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt['contractAddress']

    def send(self, abi, address, function_name, *args):
        acct = self.w3.eth.account.privateKeyToAccount(
            "0x81ab836599c179fadf202e1ccdb61e386a3bd72f1d8fc200aa3e19422b57bf11")
        self.w3.eth.default_account = acct

        contract = self.w3.eth.contract(
            abi=abi,
            address=address
        )
        function_txn = contract.functions[function_name](*args).buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 210000,
            'gasPrice': self.w3.toWei('22', 'gwei')})

        signed = acct.signTransaction(function_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def call(self, abi, address, function_name, *args):
        contract = self.w3.eth.contract(
            abi=abi,
            address=address
        )
        result = contract.functions[function_name](*args).call({})

        print(result)
        return result