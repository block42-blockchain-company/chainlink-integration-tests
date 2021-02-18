import json
import os
import sys
import urllib
import solc

from logging import Logger
from pathlib import Path

log = Logger("SolidityController")

def solidity_platform():
    if sys.platform == 'linux':
        platform = 'linux-amd64'
    elif sys.platform == 'darwin':
        platform = 'macosx-amd64'
    else:
        log.debug("Unsupported platform.")
        sys.exit(1)
    return platform


def get_available_versions():
    url = f"https://binaries.soliditylang.org/{solidity_platform()}/list.json"
    list_json = urllib.request.urlopen(url).read()
    return json.loads(list_json)["releases"]


def create_dir_if_not_exists(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)


def create_file_if_not_exists(path):
    file = open(path, 'w+')
    file.close()


class SolidityController:

    def __init__(self, solc_veresion):
        self.install_compiler(solc_veresion)

    def install_compiler(self, version):
        releases = get_available_versions()
        if releases[version] is not None:
            url = f"https://binaries.soliditylang.org/{solidity_platform()}/{releases[version]}"
            artifact_file = f"./solc/solc"
            create_dir_if_not_exists("./solc")
            create_file_if_not_exists("./solc/solc")
            log.debug(f"Installing '{version}'...")
            urllib.request.urlretrieve(url, artifact_file)
            os.chmod(artifact_file, 0o775)
            log.debug(f"Version '{version}' installed.")
        else:
            log.debug(f"Version '{version}' not exists.")

    def compile(self, path):
        paths = []
        for p in Path(path).rglob('*.sol'):
            paths.append(p.as_posix())
        self.compiled_contracts = solc.compile_files(source_files=paths, solc_binary="./solc/solc")

    def deploy(self, contract_name, chain_controller, *args, **kwargs):
        contract = self.compiled_contracts.get(contract_name)
        return chain_controller.deploy_contract(contract, *args, **kwargs)
