import time
import unittest
from logging import Logger
from chainlink.ChainlinkController import ChainlinkController
from fantom.FanomController import FantomController
from solidity.SolidityController import SolidityController
from definitions import ROOT_DIR

log = Logger(name="Test_FantomChainlinkIntegration")

class Test_FantomChainlinkIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        log.debug("Setup")
        log.debug("\t\tfantom docker")
        self.fantom_controller = FantomController()
        self.fantom_controller.docker_build()
        self.fantom_controller.docker_run_fantom("fantom_lachesis")

        log.debug("\t\tchainlink docker")
        self.chainlink_controller = ChainlinkController()
        self.chainlink_controller.docker_run_chainlink("chainlink_chainlink")

        log.debug("\t\twait for docker startup")
        time.sleep(2)
        log.debug("/Setup")

    @classmethod
    def tearDownClass(self) -> None:
        log.debug("Teardown")
        log.debug("\t\tstop fantom")
        self.fantom_controller.docker_stop("fantom_lachesis")
        self.fantom_controller.docker_rm("fantom_lachesis")
        self.fantom_controller.docker_rmi()

        log.debug("\t\tstop chainlink")
        self.chainlink_controller.docker_stop("chainlink_chainlink")
        self.chainlink_controller.docker_rm("chainlink_chainlink")
        log.debug("/Teardown")

    def test_compile_contracts(self):
        log.debug("test_compile_contracts")
        log.debug("\t\tinstall solc 0.4.11")
        self.solidity_controller = SolidityController("0.4.11")
        log.debug("\t\tcompile/deploy LinkToken")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/LinkToken")
        link_address = self.solidity_controller.deploy(ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken",
                                                       self.fantom_controller)
        log.debug("\t\tLink address: " + link_address)
        log.debug("\t\tinstall solc 0.4.24")
        self.solidity_controller = SolidityController("0.4.24")
        self.solidity_controller.compile(ROOT_DIR + "/contracts/Oracle")
        oracle_address = self.solidity_controller.deploy(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle",

                                                         self.fantom_controller, link_address)
        log.debug("\t\tOracle address: " + oracle_address)

        self.solidity_controller.compile(ROOT_DIR + "/contracts/OracleConsumer")
        api_address = self.solidity_controller.deploy(
            ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
            self.fantom_controller, link_address, oracle_address)
        log.debug("\t\tApi address: " + api_address)
        log.debug("/test_compile_contracts")


if __name__ == '__main__':
    unittest.main()
