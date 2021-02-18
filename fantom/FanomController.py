import docker
from definitions import ROOT_DIR
from web3 import Web3


class FantomController:
    DOCKER_TAG = "fantom_lachesis"
    PORT = 3001
    URL = "http://localhost"

    def __init__(self):
        self.docker_client = docker.from_env()
        self.w3 = Web3(Web3.HTTPProvider(self.URL + ":" + str(self.PORT)))

    def docker_build(self):
        self.docker_client.images.build(path=(ROOT_DIR + "/Dockerfiles/Fantom/"), tag=self.DOCKER_TAG)

    def docker_stop(self, name):
        self.docker_client.containers.get(name).stop()

    def docker_rm(self, name):
        self.docker_client.containers.get(name).remove()

    def docker_rmi(self):
        self.docker_client.images.remove(image=self.DOCKER_TAG)

    def docker_run_fantom(self, name):
        self.docker_client.containers.run(self.DOCKER_TAG, name=name, ports={self.PORT: 3001, 8535: 8535, 5050: 5050},
                                          detach=True)

    def deploy_contract(self, compiledContract, *args, **kwargs) -> None:
        # Instantiate and deploy contract
        contract = self.w3.eth.contract(
            abi=compiledContract['abi'],
            bytecode=compiledContract['bin']
        )
        # Get transaction hash from deployed contract
        tx_hash = contract.constructor(*args, **kwargs).transact({
            "gas": 500000,
            "gasLimit": 70000000,
            "skipDryRun": True,
            "from": self.w3.eth.accounts[0]
        })
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt['contractAddress']

