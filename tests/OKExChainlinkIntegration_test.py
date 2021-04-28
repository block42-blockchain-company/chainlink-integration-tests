import time
import os
import unittest
from logging import Logger

from blockchain.OKExController import OKExController
from chainlink.ChainlinkController import ChainlinkController
from definitions import ROOT_DIR
from postgres.PostgresController import PostgresController
from solidity.SolidityController import SolidityController

log = Logger(name="Test_FantomChainlinkIntegration")

class Test_OKExChainlinkIntegration(unittest.TestCase):

    GAS = 152625
    GWEI = 1

    @classmethod
    def setUpClass(self) -> None:
        log.debug("Setup")
        self.okexchain_controller = OKExController()
        self.okexchain_controller.create_network("integration-tests")

        self.postgres_controller = PostgresController()
        self.postgres_controller.docker_run("chainlink_postgres")
        time.sleep(5)
        self.postgres_controller.init_db("chainlink")

        self.solidity_controller = SolidityController("v0.4.11")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/LinkToken")
        self.link_address = self.solidity_controller.deploy(
            os.environ["PK_OKEx"],
            ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken",
            self.okexchain_controller)
        self.link_contract = self.solidity_controller.getContract(
            ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
        print("LINK: " + self.link_address)

        self.chainlink_controller = ChainlinkController(link_address=self.link_address,
                                                        eth_url="ws://18.167.77.79:8546",
                                                        chain_id=65)
        self.chainlink_controller.docker_run("chainlink_chainlink")

        log.debug("\t\twait for docker startup")
        time.sleep(30)
        log.debug("/Setup")
        return

    @classmethod
    def tearDownClass(self) -> None:
        log.debug("Teardown")
        log.debug("\t\tstop chainlink")
        self.chainlink_controller.docker_stop("chainlink_chainlink")
        self.chainlink_controller.docker_rm("chainlink_chainlink")

        log.debug("\t\tstop postgres")
        self.chainlink_controller.docker_stop("chainlink_postgres")
        self.chainlink_controller.docker_rm("chainlink_postgres")
        log.debug("/Teardown")

    def test_integrate_okex(self):
        log.debug("test_compile_contracts")

        log.debug("\t\tinstall solc 0.4.24")
        self.solidity_controller = SolidityController("v0.4.24")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/Oracle")
        oracle_contract = self.solidity_controller.getContract(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle")
        oracle_address = self.solidity_controller.deploy(
            os.environ["PK_OKEx"],
            ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle",
            self.okexchain_controller, self.link_address)
        print("Oracle: " + oracle_address)

        self.solidity_controller.compile(ROOT_DIR + "/contracts/OracleConsumer")
        time.sleep(10)
        api_address = self.solidity_controller.deploy(
            os.environ["PK_OKEx"],
            ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
            self.okexchain_controller, self.link_address)
        print("TEST API: " + api_address)
        time.sleep(10)
        self.okexchain_controller.send(
            os.environ["PK_OKEx"],
            self.link_contract["abi"], self.link_address, "transfer", self.GAS, api_address,
            2 * (10 ** 18))

        api_contract = self.solidity_controller.getContract(
            ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")

        time.sleep(10)
        chainlink_address = self.chainlink_controller.get_chainlink_address(0)
        self.okexchain_controller.sendToken(os.environ["PK_OKEx"], (2 * (10 ** 18)), chainlink_address, gas=self.GAS)
        time.sleep(10)
        chainlink_address = self.chainlink_controller.get_chainlink_address(1)
        self.okexchain_controller.sendToken(os.environ["PK_OKEx"], (2 * (10 ** 18)), chainlink_address, gas=self.GAS)

        chainlink_address = self.chainlink_controller.get_chainlink_address(0)
        time.sleep(10)
        self.okexchain_controller.send(
            os.environ["PK_OKEx"],
            self.link_contract["abi"], self.link_address, "transfer", self.GAS,
            chainlink_address, 2 * (10 ** 18))
        time.sleep(10)
        self.okexchain_controller.send(
            os.environ["PK_OKEx"],
            oracle_contract["abi"], oracle_address, "setFulfillmentPermission", self.GAS,
            chainlink_address, True)

        time.sleep(10)
        chainlink_job_id = self.chainlink_controller.init_job(oracle_address)
        print("jobid: " + chainlink_job_id)
        time.sleep(30)
        self.okexchain_controller.send(
            os.environ["PK_OKEx"],
            api_contract["abi"], api_address, "requestEthereumPrice", self.GAS,
            self.okexchain_controller.w3.toChecksumAddress(oracle_address),
            chainlink_job_id)

        time.sleep(30)
        result = self.okexchain_controller.call(
            os.environ["PK_OKEx"],
            api_contract["abi"], api_address, "currentPrice")
        self.assertTrue(int(result) > 0)
