from typing import List


class IServiceController:
    """Interfaces for a controller that manages the lifecycle and state of a service"""

    def get_status(self):
        """Get the current status of the service"""
        raise NotImplementedError

    # State transitions

    def deploy(self):
        raise NotImplementedError

    def upgrade(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def scale(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError

    def backup(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    # Settings interaction

    def get_config(self):
        raise NotImplementedError

    def set_config(self):
        raise NotImplementedError

    def get_secrets(self):
        raise NotImplementedError

    def set_secrets(self):
        raise NotImplementedError

    def get_env(self):
        raise NotImplementedError

    def set_env(self):
        raise NotImplementedError

    # Retriving data

    def get_logs(self) -> List[str]:
        raise NotImplementedError

    def get_metrics(self) -> List[str]:
        raise NotImplementedError

    def get_events(self) -> List[str]:
        raise NotImplementedError

    def get_resources(self):
        raise NotImplementedError

    def monitor(self):
        raise NotImplementedError

    # Store log

    def alert(self, message):
        raise NotImplementedError

    def notify(self, message):
        raise NotImplementedError

    def log(self, message):
        raise NotImplementedError
