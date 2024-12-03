from django.conf import settings
from viewflow.fsm import State
from django.utils.translation import gettext_lazy as _

from .interfaces import IBillingController, IServiceController
from .models import Service
from usop.apps.services.status import ServiceStatus
import subprocess


class DefaultBillingController(IBillingController): 
    """ Reimplement this class to allow billing for services """   
    def can_deploy(self, service):
        return True
    

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
        billing_ok = self.service.get_billing_controller().can_deploy(self.service)
        if not billing_ok:
            raise Exception(_("Billing failed"))
        helm_command = [
            "helm", "upgrade", "--install", "--atomic",]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.UPGRADING, target=ServiceStatus.RUNNING)
    def upgrade(self):
        """ Upgrade the service to the latest version of the chart """        
        billing_ok = self.service.get_billing_controller().can_deploy(self.service)
        if not billing_ok:
            raise Exception(_("Billing failed"))
        helm_command = [
            "helm", "upgrade", "--install", "--reuse-values", "--atomic"]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        helm_command += [
            str(self.service.pid),
            self.service.template,
            "--namespace", self.service.namespace
        ]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
        
    @state.transition(source=ServiceStatus.RUNNING, target=ServiceStatus.STOPPED)
    def stop(self):
        """ Stop the service by deleting the running pod """
        helm_command = [
            "helm", "delete"]
        helm_command += [
            str(self.service.pid),
            "--namespace", self.service.namespace,
            "--wait"
        ]
        if settings.DEBUG:
            helm_command += ["--debug"]
        if settings.DRY_RUN:
            helm_command += ["--dry-run"]
        result = subprocess.run(helm_command, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Helm command failed with return code {result.returncode}: {result.stderr}")
    