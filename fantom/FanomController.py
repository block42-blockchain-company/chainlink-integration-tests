import docker


class FantomController:

    DOCKER_TAG = "fantom_lachesis"

    def __init__(self):
        print("init FantomController")
        self.docker_client = docker.from_env()

    def docker_build(self):
        self.docker_client.images.build(path=("./Dockerfiles/Fantom/"), tag=self.DOCKER_TAG)

    def docker_stop(self, name):
        self.docker_client.containers.get(name).stop()

    def docker_rm(self, name):
        self.docker_client.containers.get(name).remove()

    def docker_rmi(self):
        self.docker_client.images.remove(image=self.DOCKER_TAG)

    def docker_run_fantom(self, name):
        print("docker run fantom " + name)
        self.docker_client.containers.run(self.DOCKER_TAG, name=name, ports={3001: 3001, 8535: 8535, 5050: 5050}, detach=True)