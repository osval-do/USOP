from django.conf import settings
from viewflow.fsm import State
from django.utils.translation import gettext_lazy as _

from .interfaces import IServiceController
from .models import Service
from usop.apps.services.status import ServiceStatus
import subprocess

class ServiceController(IServiceController):
    state = State(ServiceStatus, default=ServiceStatus.NEW)
    service: Service
    
    def __init__(self, service):
        self.service = service

    @state.setter()
    def _set_state(self, value):
        self.report.service = value

    @state.getter()
    def _get_state(self):
        return self.service.status
    
    @state.on_success()
    def _on_transition_success(self, descriptor, source, target):
        """ Save the service after a successful transition """
        self.service.save()
        
    def get_status(self):
        """ Get the current status of the service """
        return self.service.status

    @state.transition(source=ServiceStatus.NEW, target=ServiceStatus.RUNNING)
    def deploy(self):
        """ Deploy the service in the target region """
        helm_command = settings.HELM_COMMAND + ["upgrade", "--install", "--atomic",]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.org.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.UPGRADING, target=ServiceStatus.RUNNING)
    def upgrade(self):
        """ Upgrade the service to the latest version of the chart """
        helm_command = settings.HELM_COMMAND + ["--install", "--reuse-values", "--atomic"]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.org.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.RUNNING, target=ServiceStatus.STOPPED)
    def stop(self):
        """ Stop the service by deleting the running pod """
        # TODO switch this to use helm delete
        kubectl_command = settings.KUBECTL_COMMAND + [
            "delete", "pod", str(self.service.pid),
            "--namespace", self.service.org.namespace
        ]
        result = subprocess.run(kubectl_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Kubectl command failed with return code {result.returncode}: {result.stderr}")
    
    @state.transition(source=ServiceStatus.RUNNING, target=ServiceStatus.RUNNING)
    def restart(self):
        """ Restart the service """
        self.stop()
        self.deploy()
        
    @state.transition(source=ServiceStatus.RUNNING, target=ServiceStatus.ROLLING_BACK)
    def rollback(self):
        """ Rollback the service to the previous version """
        helm_command = settings.HELM_COMMAND + ["rollback", "0", str(self.service.pid)]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += ["--namespace", self.service.org.namespace]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm rollback command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(target=ServiceStatus.DESTROYED)
    def destroy(self):
        """ Destroy the service and all its resources from the cluster """
        helm_command = settings.HELM_COMMAND + ["delete", str(self.service.pid)]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += ["--namespace", self.service.org.namespace]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm delete command failed with return code {result.returncode}: {result.stderr}")
        

    
    