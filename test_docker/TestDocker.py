from docker_helper.Dockerabstract import Dockerabstract


class TestDocker(Dockerabstract):
    DOCKERFILE_DIR = "/Dockerfiles/TestRestApi"
    DOCKER_TAG = "test"
    DOCKER_PORTS = {8000: 8000}

    def __init__(self):
        super().__init__()