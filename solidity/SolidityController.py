import json
import os
import sys
import urllib

import solc
from pathlib import Path


def solidity_platform():
    if sys.platform == 'linux':
        platform = 'linux-amd64'
    elif sys.platform == 'darwin':
        platform = 'macosx-amd64'
    else:
        print("Unsupported platform.")
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

    def install_compiler(self, version):
        releases = get_available_versions()
        if releases[version] != None:
            url = f"https://binaries.soliditylang.org/{solidity_platform()}/{releases[version]}"
            artifact_file = f"./solc/solc"
            create_dir_if_not_exists("./solc")
            create_file_if_not_exists("./solc/solc")
            print(f"Installing '{version}'...")
            urllib.request.urlretrieve(url, artifact_file)
            os.chmod(artifact_file, 0o775)
            print(f"Version '{version}' installed.")
        else:
            print(f"Version '{version}' not exists.")

    def compile(self, path):
        paths = []
        for p in Path(path).rglob('*.sol'):
            print(p.absolute())
            paths.append(p.as_posix())
        self.compiled_contracts = solc.compile_files(source_files=paths, solc_binary="./solc/solc")
