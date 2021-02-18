import docker


class ChainlinkController:

    DOCKER_TAG = 'smartcontract/chainlink:0.9.4'

    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_client.images.pull(self.DOCKER_TAG)

    def docker_run_chainlink(self, name):
        self.docker_client.containers.run(self.DOCKER_TAG, name=name, ports={6688: 6688},
                                          detach=True)

    def docker_stop(self, name):
        self.docker_client.containers.get(name).stop()

    def docker_rm(self, name):
        self.docker_client.containers.get(name).remove()
