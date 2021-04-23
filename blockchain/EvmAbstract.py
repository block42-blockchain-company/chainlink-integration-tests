import os

from web3 import Web3


class EvmAbstract():

    def deploy_contract(self, abi, bytecode, *args, **kwargs) -> None:
        contract_ = self.w3.eth.contract(
            abi=abi,
            bytecode=bytecode
        )
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        print("Sender address:" + acct.address)
        construct_txn = contract_.constructor(*args, **kwargs).buildTransaction({
            'from': acct.address,
            'nonce': self.w3.eth.getTransactionCount(acct.address),
            'gas': 6883720,
            'gasPrice': self.w3.toWei('1', 'gwei')})
        signed = acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt['contractAddress']

    def send(self, abi, address, function_name, gas, *args):
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
            'gas': gas,
            'gasPrice': self.w3.toWei('2', 'gwei')})

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

    def sendToken(self, _amount, _to, gas=7000000):
        print("send token to " + _to)
        acct = self.w3.eth.account.privateKeyToAccount(
            os.environ["PK"])
        self.w3.eth.default_account = acct
        signed = self.w3.eth.account.signTransaction(
            {
                'to': self.w3.toChecksumAddress(_to),
                'from': self.w3.toChecksumAddress(acct.address),
                'value': _amount,
                'nonce': self.w3.eth.getTransactionCount(acct.address),
                'gas': gas,
                'gasPrice': self.w3.toWei(1, 'gwei')
            }, os.environ["PK"])
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_rec = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_rec)
        print("status: " + str(tx_rec["status"]))
