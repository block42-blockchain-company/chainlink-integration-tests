from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from definitions import ROOT_DIR
from docker_helper.Dockerabstract import Dockerabstract
import psycopg2


class PostgresController(Dockerabstract):
    DOCKER_TAG = "postgres"
    DOCKER_ENV = {"POSTGRES_PASSWORD": "postgres"}
    DOCKER_VOLUMES = [ROOT_DIR + "/postgresql_config:/etc/postgresql"]
    DOCKER_PORTS = {"5432": 5432}
    DOCKER_COMMAND = "-c config_file=/etc/postgresql/postgresql.conf"

    def init_db(self, database):
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password=self.DOCKER_ENV['POSTGRES_PASSWORD'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE {database};')
