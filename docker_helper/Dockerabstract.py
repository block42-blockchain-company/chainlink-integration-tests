import docker
from definitions import ROOT_DIR


class Dockerabstract:
    DOCKER_TAG = None
    DOCKER_ENV = {}
    DOCKER_PORTS = {}
    DOCKERFILE_DIR = "/"
    DOCKER_COMMAND = ""
    DOCKER_VOLUMES = []

    def __init__(self):
        self.docker_client = docker.from_env()

    def create_network(self, name):
        networks = self.docker_client.networks.list()
        for n in networks:
            if n.name == name:
                return
        self.docker_client.networks.create(name)

    def docker_build(self):
        self.docker_client.images.build(path=(ROOT_DIR + self.DOCKERFILE_DIR), tag=self.DOCKER_TAG)

    def docker_run(self, name):
        self.docker_client.containers.run(self.DOCKER_TAG,
                                          name=name,
                                          detach=True,
                                          ports=self.DOCKER_PORTS,
                                          network="integration-tests",
                                          environment=self.DOCKER_ENV,
                                          command=self.DOCKER_COMMAND,
                                          volumes=self.DOCKER_VOLUMES)

    def docker_stop(self, name):
        self.docker_client.containers.get(name).stop()

    def docker_rm(self, name):
        self.docker_client.containers.get(name).remove()

    def docker_rmi(self):
        self.docker_client.images.remove(image=self.DOCKER_TAG)