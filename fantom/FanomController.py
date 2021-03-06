import os
from web3 import Web3
from docker_helper.Dockerabstract import Dockerabstract


class FantomController(Dockerabstract):
    DOCKER_TAG = "fantom_lachesis"
    DOCKER_PORTS = {3001: 3001, 8546: 8546, 5050: 5050}
    DOCKERFILE_DIR = "/Dockerfiles/Fantom/"
    URL = "http://localhost"
    URL_TESTNET = "https://rpcapi.fantom.network"

    def __init__(self, mainnet=False):
        if mainnet:
            self.w3 = Web3(Web3.HTTPProvider(self.URL_TESTNET))
        else:
            self.w3 = Web3(Web3.HTTPProvider(self.URL + ":" + str(3001)))
        super().__init__()

    def sendFtm(self, _amount, _to):
        print("send fantom to " + _to)
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        self.w3.eth.default_account = acct
        signed = self.w3.eth.account.signTransaction(
            {
                'to': self.w3.toChecksumAddress(_to),
                'from': self.w3.toChecksumAddress(acct.address),
                'value': _amount,
                'nonce': self.w3.eth.getTransactionCount(acct.address),
                'gas': 7000000,
                'gasPrice': self.w3.toWei('22', 'gwei')
            }, os.environ["PK"])
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_rec = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_rec)
        print("status: " + str(tx_rec["status"]))

    def deploy_contract(self, abi, bytecode, *args, **kwargs) -> None:
        contract_ = self.w3.eth.contract(
            abi=abi,
            bytecode=bytecode
        )
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        construct_txn = contract_.constructor(*args, **kwargs).buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 7000000,
            'gasPrice': self.w3.toWei('21', 'gwei')})
        signed = acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt['contractAddress']

    def send(self, abi, address, function_name, *args):
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        self.w3.eth.default_account = acct.address

        contract = self.w3.eth.contract(
            abi=abi,
            address=self.w3.toChecksumAddress(address)
        )
        function_txn = contract.functions[function_name](*args).buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 7000000,
            'gasPrice': self.w3.toWei('22', 'gwei')})

        signed = acct.signTransaction(function_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def call(self, abi, address, function_name, *args):
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        self.w3.eth.default_account = acct.address
        contract = self.w3.eth.contract(
            abi=abi,
            address=self.w3.toChecksumAddress(address)
        )
        result = contract.functions[function_name](*args).call({
            "from": acct.address
        })

        print(result)
        return result