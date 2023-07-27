"""
All of the docker related stuff
"""

import docker
import asyncio


class Docker:
    def __init__(self):
        self.docker = docker.from_env()

    def create(self, userbot, port, name):
        self.docker.containers.run(
            f"lumi{userbot}:latest",
            cpu_period=50000,
            cpu_quota=25000,
            mem_limit="1g",
            name=str(name),
            ports={8080: port},
            detach=True,
            tty=True,
        )

    async def wait_for_output(self, name, expected_output):
        """Looks horrible"""
        attempts = 10

        while attempts > 0:
            attempts -= 1

            if any([expected_output in x for x in self.get(name).logs().split("\n")]):
                return True
            await asyncio.sleep(3)
        return False

    def stop(self, name):
        self.docker.containers.get(name).stop(timeout=1)

    def start(self, name):
        self.docker.containers.get(name).start()

    def restart(self, name):
        # await asyncio.sleep(0.1)
        self.docker.containers.get(name).restart(timeout=1)

    def remove(self, name):
        self.docker.containers.get(name).remove(v=True, force=True)

    def execute(self, name, command):
        try:
            return self.docker.containers.get(name).exec_run(command, tty=True, workdir='/Hikka')
        except Exception:
            return None

    def get(self, name):
        try:
            return self.docker.containers.get(name)
        except docker.errors.NotFound:
            return None
