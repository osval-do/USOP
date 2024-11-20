from django.conf import settings
from viewflow.fsm import State
from django.utils.translation import gettext_lazy as _

from .models import Service
from usop.apps.services.status import ServiceStatus
import subprocess

class ServiceFSM(object):
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

    @state.transition(source=ServiceStatus.NEW, target=ServiceStatus.RUNNING)
    def deploy(self):
        """ Deploy the service in the target region """
        helm_command = [
            "helm", "upgrade", "--install", "--atomic",]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.region.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.UPGRADING, target=ServiceStatus.RUNNING)
    def upgrade(self):
        """ Upgrade the service to the latest version of the chart """
        helm_command = [
            "helm", "upgrade", "--install", "--reuse-values", "--atomic"]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.region.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.RUNNING, target=ServiceStatus.STOPPED)
    def stop(self):
        """ Stop the service by deleting the running pod """
        kubectl_command = [
            "kubectl", "delete", "pod", str(self.service.pid),
            "--namespace", self.service.region.namespace
        ]
        result = subprocess.run(kubectl_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Kubectl command failed with return code {result.returncode}: {result.stderr}")
    
    