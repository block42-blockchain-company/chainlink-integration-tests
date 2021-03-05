import time

from definitions import ROOT_DIR
from fantom.FanomController import FantomController
from solidity.SolidityController import SolidityController
from test_docker.TestDocker import TestDocker


def call():
    fantom_ctrl = FantomController()
    #solidity_ctrl = SolidityController("v0.4.25")
    #solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    #link_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken", fantom_ctrl)
    #print(link_addr)

    #link_addr = "0xD171858f109Ea35cf2652825e9483146870D79CE"

    solidity_ctrl = SolidityController("v0.4.24")
    #solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    #oracle_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", fantom_ctrl, link_addr)

    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    #test_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer", fantom_ctrl, link_addr, oracle_addr)
    api_test_consumer = solidity_ctrl.getContract(ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    fantom_ctrl.send(api_test_consumer["abi"], "0xd9d0C8Dcc8D1d2b3a87dfFC3711E8e5b608A15b4", "accpectChainLinkRequest", "f40fdc0bc1c74f1c846c5ac6c1f121d9")
    fantom_ctrl.call(api_test_consumer["abi"], "0xd9d0C8Dcc8D1d2b3a87dfFC3711E8e5b608A15b4", "getMyTest")

def deploy_link_oracle_api():
    fantom_ctrl = FantomController()
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken", fantom_ctrl)
    print("link: " + link_addr)

    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    oracle_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", fantom_ctrl, link_addr)

    print("oracle: " + oracle_addr)

    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    test_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer", fantom_ctrl, link_addr, oracle_addr)

    print("test: " + test_addr)

def deploy_test_api():
    fantom_ctrl = FantomController(True)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    test_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer",
                                     fantom_ctrl, "0x6F43FF82CCA38001B6699a8AC47A2d0E66939407")
    #"0x0a0f4b0D23F423E1e64100D0C2102f71E079B096", "0x234256711dB1e916c51aEcf1DF6351bcf246a24d"
    print(test_addr)

def call_deployt_api_test():
    fantom_ctrl = FantomController(True)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    api_test_consumer = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    fantom_ctrl.send(api_test_consumer["abi"], "0xEB7B1605eB5312B1c160730b900DF03fDB7C2C90", "requestEthereumPrice",
                     fantom_ctrl.w3.toChecksumAddress("0x234256711dB1e916c51aEcf1DF6351bcf246a24d"), "39174b95f7f74d85a448927e0dcf2bf9")
    #fantom_ctrl.call(api_test_consumer["abi"], "0xd9d0C8Dcc8D1d2b3a87dfFC3711E8e5b608A15b4", "getMyTest")

def call_deployt_api_test_current_price():
    fantom_ctrl = FantomController(True)
    solidity_ctrl = SolidityController("v0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/OracleConsumer/")
    api_test_consumer = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/OracleConsumer/APITestConsumer.sol:APITestConsumer")
    fantom_ctrl.call(api_test_consumer["abi"], "0xEB7B1605eB5312B1c160730b900DF03fDB7C2C90", "currentPrice")


def fund_test_api_contract():
    fantom_ctrl = FantomController()
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_contract = solidity_ctrl.getContract(ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
    fantom_ctrl.send(link_contract["abi"], "0x86989606A88841E2Fb56787806a5f7a3A89641e2", "transfer", "0x2852C2B1de66488B6C98659Ff9BE482FF572E5cc", 100 * (10 ** 18))

def deploy_oracle_testnet():
    fantom_ctrl = FantomController(True)

    solidity_ctrl = SolidityController("0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    contract_addr = solidity_ctrl.deploy(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle", fantom_ctrl, "0x6F43FF82CCA38001B6699a8AC47A2d0E66939407")
    print(contract_addr)

def balanceof():
    # balanceOf
    fantom_ctrl = FantomController(True)
    solidity_ctrl = SolidityController("v0.4.25")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/LinkToken")
    link_contract = solidity_ctrl.getContract(
        ROOT_DIR + "/contracts/LinkToken/LinkToken.sol:LinkToken")
    fantom_ctrl.call(link_contract["abi"], "0x0a0f4b0D23F423E1e64100D0C2102f71E079B096", "balanceOf", "0x234256711dB1e916c51aEcf1DF6351bcf246a24d")

def start_fantom_and_chainlinkpostgres():
    #fantom_controller = FantomController()
    #fantom_controller.create_network("integration-tests")
    #fantom_controller.docker_build()
    #fantom_controller.docker_run("fantom_lachesis")

    test_docker = TestDocker()
    test_docker.docker_build()
    test_docker.docker_run("rest-test")

    #postgres_controller = PostgresController()
    #postgres_controller.docker_run("chainlink_postgres")
    #time.sleep(10)
    #postgres_controller.init_db("chainlink")

def fund():
    #link: 0x50793EFE14fB7e2Ca216A6275E2d8028be8C0A65
    #oracle: 0xCB32b0540739d965FdcfC7d5A56C14ecD467D4b2
    #test: 0x7a742c7dF88926b17677fC98D60fBa1967532114
    fantom_controller = FantomController()
    fantom_controller.sendFtm((100 * (10 ** 18)), "0xE7d1aaa95096eFe676682F35e0e566AA1ff8C432")

def set_fullfilment_permission():
    fantom_controller = FantomController(True)
    solidity_ctrl = SolidityController("0.4.24")
    solidity_ctrl.compile(ROOT_DIR + "/contracts/Oracle/")
    oracle_contract = solidity_ctrl.getContract(ROOT_DIR + "/contracts/Oracle/Oracle.sol:Oracle")
    fantom_controller.send(oracle_contract["abi"], "0x234256711dB1e916c51aEcf1DF6351bcf246a24d",
                           "setFulfillmentPermission", "0x3fD381B7308B614e993a4941e60809d7F83563a6", True)

if __name__ == '__main__':
    #start_fantom_and_chainlinkpostgres()
    #time.sleep(3)
    #deploy_test_api()
    #fund()
    #deploy_oracle_testnet()
    #time.sleep(90)
    call_deployt_api_test()
    time.sleep(15)
    call_deployt_api_test_current_price()
    #deploy_oracle_testnet()
    #fund_test_api_contract()
    #balanceof()
    #set_fullfilment_permission()