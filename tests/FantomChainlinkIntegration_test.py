import time
import os
import unittest
from logging import Logger
from chainlink.ChainlinkController import ChainlinkController
from blockchain.FanomController import FantomController
from postgres.PostgresController import PostgresController
from solidity.SolidityController import SolidityController
from definitions import ROOT_DIR

log = Logger(name="Test_FantomChainlinkIntegration")


class Test_FantomChainlinkIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        log.debug("Setup")
        log.debug("\t\tblockchain docker")
        self.fantom_controller = FantomController()
        self.fantom_controller.create_network("integration-tests")
        self.fantom_controller.docker_build()
        self.fantom_controller.docker_run("fantom_lachesis")

        self.postgres_controller = PostgresController()
        self.postgres_controller.docker_run("chainlink_postgres")
        time.sleep(5)
        self.postgres_controller.init_db("chainlink")

        self.solidity_controller = SolidityController("v0.4.11")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/LinkToken")
        self.link_address = self.solidity_controller.deploy(os.environ["PK_FTM"],
                                                            ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken",
                                                            self.fantom_controller)
        self.link_contract = self.solidity_controller.getContract(
            ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
        print("LINK: " + self.link_address)

        self.chainlink_controller = ChainlinkController(link_address=self.link_address)
        self.chainlink_controller.docker_run("chainlink_chainlink")

        log.debug("\t\twait for docker startup")
        time.sleep(30)
        log.debug("/Setup")

    @classmethod
    def tearDownClass(self) -> None:
        log.debug("Teardown")
        log.debug("\t\tstop blockchain")
        self.fantom_controller.docker_stop("fantom_lachesis")
        self.fantom_controller.docker_rm("fantom_lachesis")
        self.fantom_controller.docker_rmi()

        log.debug("\t\tstop chainlink")
        self.chainlink_controller.docker_stop("chainlink_chainlink")
        self.chainlink_controller.docker_rm("chainlink_chainlink")

        log.debug("\t\tstop postgres")
        self.chainlink_controller.docker_stop("chainlink_postgres")
        self.chainlink_controller.docker_rm("chainlink_postgres")
        log.debug("/Teardown")

    def test_compile_contracts(self):
        log.debug("test_compile_contracts")

        log.debug("\t\tinstall solc 0.4.24")
        self.solidity_controller = SolidityController("v0.4.24")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/Oracle")
        oracle_contract = self.solidity_controller.getContract(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle")
        oracle_address = self.solidity_controller.deploy(os.environ["PK_FTM"],
                                                         ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle",
                                                         self.fantom_controller, self.link_address)
        print("Oracle: " + oracle_address)

        self.solidity_controller.compile(ROOT_DIR + "/contracts/OracleConsumer")
        api_address = self.solidity_controller.deploy(
            os.environ["PK_FTM"],
            ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
            self.fantom_controller, self.link_address)
        print("TEST API: " + api_address)

        self.fantom_controller.send(
            os.environ["PK_FTM"],
            self.link_contract["abi"], self.link_address, "transfer", 7000000,
            api_address, 100 * (10 ** 18))

        api_contract = self.solidity_controller.getContract(
            ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")

        time.sleep(10)
        chainlink_address = self.chainlink_controller.get_chainlink_address(0)
        self.fantom_controller.sendToken(os.environ["PK_FTM"], (100 * (10 ** 18)), chainlink_address)

        chainlink_address = self.chainlink_controller.get_chainlink_address(1)
        self.fantom_controller.sendToken(os.environ["PK_FTM"], (100 * (10 ** 18)), chainlink_address)

        chainlink_address = self.chainlink_controller.get_chainlink_address(0)

        self.fantom_controller.send(
            os.environ["PK_FTM"],
            self.link_contract["abi"], self.link_address, "transfer", 7000000,
            chainlink_address,
            100 * (10 ** 18))
        self.fantom_controller.send(
            os.environ["PK_FTM"],
            oracle_contract["abi"], oracle_address, "setFulfillmentPermission", 7000000,
            chainlink_address, True)

        time.sleep(10)
        chainlink_job_id = self.chainlink_controller.init_job(oracle_address)
        print("jobid: " + chainlink_job_id)
        time.sleep(30)
        self.fantom_controller.send(
            os.environ["PK_FTM"],
            api_contract["abi"], api_address, "requestEthereumPrice", 7000000,
            self.fantom_controller.w3.toChecksumAddress(oracle_address), chainlink_job_id)

        time.sleep(30)
        result = self.fantom_controller.call(
            os.environ["PK_FTM"],
            api_contract["abi"], api_address, "currentPrice")
        self.assertTrue(int(result) > 0)


if __name__ == '__main__':
    unittest.main()
