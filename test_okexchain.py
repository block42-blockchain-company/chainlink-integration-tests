import time
import os
from blockchain.OKExController import OKExController
from chainlink.ChainlinkController import ChainlinkController
from definitions import ROOT_DIR
from blockchain.FanomController import FantomController
from postgres.PostgresController import PostgresController
from solidity.SolidityController import SolidityController
from test_docker.TestDocker import TestDocker

LINK_ADDR_mainnet = "0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8"
LINK_ADDR = "0xdB2E501f4637c081b87c91b3aFB1A19BB52d6AFe"
ORACLE_TEST_ADDR_mainnet = "0x86DA0b44203C2EC2316ba18d8D372d0E3eCc274e"  # "0x45d23Ba4fD7eabe011C852eEc65299655BC08F5D" # "0x804f5882A0dEb9088Df47Bc64851D898C015B80f" #0x804f5882A0dEb9088Df47Bc64851D898C015B80f
ORACLE_TEST_ADDR = "0x3D7B73aa91c9DD8E096fd5Cc2336cEC58f74de96" #"0x3D7B73aa91c9DD8E096fd5Cc2336cEC58f74de96"
ORACLE_ADDR_mainnet = "0x2a940e790dDb65127f4042aCDd08822F6EA83c87"  # "0xBB11CC8451e04558a6495bDae05E554525E23aAD"
ORACLE_ADDR = "0x5d3E58c0c1CcECF18B1EDA0fA9973f53ef24e078"
CHAINLINK_NODE_ADDR = "0x62e0b088E158062719Eb23604405c3f60033A33b"
CHAINLINK_NODE_ADDR_fakenet = "0x3035dA60BE31559f6B50a80968BF3e78b0423615"
CHAINLINK_JOBID_mainnet = "8e7bbf04e3ad4676896b54fa81ed582c"
CHAINLINK_JOBID = "dd52751f6a994540be623c12698c093a"
OWNER_ADDR = "0xc353877977b79E13DdF7dd67CF8C3c5C2DF3C893"
MAINNET = False


def test_chainlink_integration():
    fantom_ctrl = FantomController(MAINNET)

    # solidity_ctrl = SolidityController("v0.8.1")
    # solidity_ctrl.compile(ROOT_DIR + "/contracts/WrappedLinkToken")
    # link_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/WrappedLinkToken/LinkToken.sol:ChainLink", fantom_ctrl,
    #                                 "LINK", "LINK", 18, fantom_ctrl.w3.toChecksumAddress(OWNER_ADDR))

    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    oracle_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", fantom_ctrl,
                                       fantom_ctrl.w3.toChecksumAddress(LINK_ADDR))
    print("Oracle: " + oracle_addr)  # 0x2ab0D4e6b968844B55a20200e8Fc3Dd6dAa29998
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    test_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
                                     fantom_ctrl, fantom_ctrl.w3.toChecksumAddress(LINK_ADDR))
    print("Test: " + test_addr)  # 0xd897A7BEDa1b5f3c1CC54F518202Ce902C8a12e0
    solidity_ctrl = SolidityController("v0.8.1")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/WrappedLinkToken")
    link_contract = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/WrappedLinkToken/LinkToken.sol:ChainLink")
    fantom_ctrl.call(os.environ["PK_OKEx"], link_contract["abi"], fantom_ctrl.w3.toChecksumAddress(LINK_ADDR), "balanceOf", OWNER_ADDR)
    fantom_ctrl.send(os.environ["PK_OKEx"], link_contract["abi"], fantom_ctrl.w3.toChecksumAddress(LINK_ADDR), "transfer",
                     test_addr, 1 * (10 ** 18))
    fantom_ctrl.call(os.environ["PK_OKEx"], link_contract["abi"], fantom_ctrl.w3.toChecksumAddress(LINK_ADDR), "balanceOf", test_addr)
    fantom_ctrl.call(os.environ["PK_OKEx"], link_contract["abi"], fantom_ctrl.w3.toChecksumAddress(LINK_ADDR), "balanceOf", OWNER_ADDR)

    # solidity_ctrl = SolidityController("v0.4.24")
    # solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")

    # api_test_consumer = solidity_ctrl.getContract(ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    # fantom_ctrl.send(api_test_consumer["abi"], test_addr, "requestEthereumPrice", fantom_ctrl.w3.toChecksumAddress(oracle_addr), CHAINLINK_JOBID)
    # time.sleep(10)
    # fantom_ctrl.call(api_test_consumer["abi"], test_addr, "currentPrice")


def deploy_link_oracle_api():
    okex_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken", okex_controller)
    print("link: " + link_addr)

    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    oracle_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", okex_controller, link_addr)

    print("oracle: " + oracle_addr)

    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    test_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
                                     okex_controller, link_addr)

    print("test: " + test_addr)


def deploy_test_api():
    okex_controller = OKExController(False)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    test_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
                                     okex_controller, LINK_ADDR)
    # "0x0a0f4b0D23F423E1e64100D0C2102f71E079B096", "0x234256711dB1e916c51aEcf1DF6351bcf246a24d"
    print(test_addr)


def call_deployt_api_test():
    okex_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    api_test_consumer = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    okex_controller.send(os.environ["PK_OKEx"], api_test_consumer["abi"], okex_controller.w3.toChecksumAddress(ORACLE_TEST_ADDR),
                         "requestEthereumPrice", 152625,
                         okex_controller.w3.toChecksumAddress(ORACLE_ADDR), CHAINLINK_JOBID)
    # fantom_ctrl.call(api_test_consumer["abi"], "0xd9d0C8Dcc8D1d2b3a87dfFC3711E8e5b608A15b4", "getMyTest")


def call_deployt_api_test_current_price():
    okexchain_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    api_test_consumer = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    okexchain_controller.call(os.environ["PK_OKEx"], api_test_consumer["abi"], ORACLE_TEST_ADDR, "currentPrice")


def fund_chainlink_node():
    okex_controller = OKExController(MAINNET)
    okex_controller.sendToken(os.environ["PK_OKEx"], 10, CHAINLINK_NODE_ADDR)

def fund_test_api_contract():
    okex_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_contract = solidity_ctrl.getContract(ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
    okex_controller.send(os.environ["PK_OKEx"], link_contract["abi"], LINK_ADDR, "transfer", 152625, ORACLE_TEST_ADDR, 10 * (10 ** 18))

def deploy_oracle_testnet():
    fantom_ctrl = FantomController(MAINNET)

    solidity_ctrl = SolidityController("0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    contract_addr = solidity_ctrl.deploy(os.environ["PK_OKEx"], ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", fantom_ctrl,
                                         fantom_ctrl.w3.toChecksumAddress(LINK_ADDR))
    print(contract_addr)


def balanceof():
    # balanceOf
    okex_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_contract = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
    okex_controller.call(os.environ["PK_OKEx"], link_contract["abi"], okex_controller.w3.toChecksumAddress(LINK_ADDR), "balanceOf",
                     okex_controller.w3.toChecksumAddress(ORACLE_TEST_ADDR))
    okex_controller.call(os.environ["PK_OKEx"], link_contract["abi"], okex_controller.w3.toChecksumAddress(LINK_ADDR), "balanceOf",
                     okex_controller.w3.toChecksumAddress(ORACLE_ADDR))


def start_fantom_and_chainlinkpostgres():
    # fantom_controller = FantomController()
    # fantom_controller.create_network("integration-tests")
    # fantom_controller.docker_build()
    # fantom_controller.docker_run("fantom_lachesis")

    test_docker = TestDocker()
    test_docker.docker_build()
    test_docker.docker_run("rest-test")

    # postgres_controller = PostgresController()
    # postgres_controller.docker_run("chainlink_postgres")
    # time.sleep(10)
    # postgres_controller.init_db("chainlink")


def fund():
    # link: 0x50793EFE14fB7e2Ca216A6275E2d8028be8C0A65
    # oracle: 0xCB32b0540739d965FdcfC7d5A56C14ecD467D4b2
    # test: 0x7a742c7dF88926b17677fC98D60fBa1967532114
    fantom_controller = OKExController()
    fantom_controller.sendToken(os.environ["PK_OKEx"], (2 * (10 ** 18)), ORACLE_TEST_ADDR)


def set_fullfilment_permission():
    okex_controller = OKExController(MAINNET)
    solidity_ctrl = SolidityController("0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    oracle_contract = solidity_ctrl.getContract(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle")
    okex_controller.send(os.environ["PK_OKEx"], oracle_contract["abi"], okex_controller.w3.toChecksumAddress(ORACLE_ADDR),
                         "setFulfillmentPermission", 700000,
                         okex_controller.w3.toChecksumAddress(CHAINLINK_NODE_ADDR),
                         True)


def withdraw_link():
    fantom_controller = FantomController(MAINNET)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    api_test_consumer = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    fantom_controller.send(os.environ["PK_OKEx"], api_test_consumer["abi"], ORACLE_TEST_ADDR, "withdrawLink")


def start_chainlinkpostgres():
    postgres_controller = PostgresController()
    postgres_controller.docker_run("chainlink_postgres")
    time.sleep(10)
    postgres_controller.init_db("chainlink")


def init_chainlink_job():
    chainlink_controller = ChainlinkController(link_address=LINK_ADDR,
                                               eth_url="ws://18.167.77.79:8546",
                                               chain_id=65)

    print(chainlink_controller.init_job(ORACLE_ADDR))
    return


if __name__ == '__main__':
    # deploy_link_oracle_api()                      # 1.
    # start_chainlinkpostgres()
    # init_chainlink_job()                          # 2. (start the chainlink node with the right LINK token before)
    # start_fantom_and_chainlinkpostgres()
    # time.sleep(3)
    # test_chainlink_integration()
    # deploy_test_api()
    # fund()
    # deploy_oracle_testnet()
    # time.sleep(90)
    # withdraw_link()
    # fund_chainlink_node()                           # 3. (after chainlink is up and running)
    fund_test_api_contract()                        # 3.
    # set_fullfilment_permission()                    # 3.
    # call_deployt_api_test()                         # 4. (set chainlink job id before)
    # time.sleep(15)
    # call_deployt_api_test_current_price()
    # deploy_oracle_testnet()

    # balanceof()
    # set_fullfilment_permission()
