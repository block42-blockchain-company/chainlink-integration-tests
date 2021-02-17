import docker


class ChainlinkController:
    def __init__(self):
        print("init ChainlinkController")
        self.docker_client = docker.from_env()
        self.docker_client.images.pull('smartcontract/chainlink:0.9.4')

    def docker_run_chainlink(self, name):
        print("docker run chainlink " + name)
        self.docker_client.containers.run("smartcontract/chainlink", name=name, ports={6688: 6688})
