# Press the green button in the gutter to run the script.
import time
import unittest

from chainlink.ChainlinkController import ChainlinkController
from fantom.FanomController import FantomController
from solidity.SolidityController import SolidityController


class Test_FantomChainlinkIntegration(unittest.TestCase):

    @classmethod
    def x_setUpClass(self) -> None:
        print("Setup")
        self.fantom_controller = FantomController()
        self.fantom_controller.docker_build()
        self.fantom_controller.docker_run_fantom("fantom_lachesis")

        #self.chainlink_controller = ChainlinkController()
        #self.chainlink_controller.docker_run_chainlink()

    def test_test(self):
        self.solidity_controller = SolidityController()
        self.solidity_controller.install_compiler("0.4.11")
        self.solidity_controller.compile("../contracts")

    @classmethod
    def x_tearDownClass(self) -> None:
        self.fantom_controller.docker_stop("fantom_lachesis")
        self.fantom_controller.docker_rm("fantom_lachesis")
        self.fantom_controller.docker_rmi()

    def test_chainlink(self):
        print("test chainlink")
        self.assertEqual("first", "first")
        print("wait for teardonw")
        time.sleep(10)




if __name__ == '__main__':
    unittest.main()
