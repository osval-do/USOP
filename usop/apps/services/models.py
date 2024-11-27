import datetime
import uuid
from django.db import models
from django.conf import settings

from .allocation import DefaultNodeAllocator, NodeAllocator
from .status import ServiceStatus
from usop.apps.users.models import Org
from .interfaces import *



class Region(models.Model):
    """A deployment area, section or group for services"""

    name: str = models.CharField(max_length=256, unique=True)
    """ Unique ID for this region """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ Creation date """

    disabled: bool = models.BooleanField()
    """ Wether to disable selecting this region for services """
    
    namespace: str = models.CharField(max_length=128, blank=True, null=True)
    """ The kubernetes namespace used for this region """

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
    def get_node_allocator(self) -> NodeAllocator:
        return DefaultNodeAllocator()


class Template(models.Model):
    """A template for a service that can be deployed in a region"""

    name: str = models.CharField(max_length=128)
    """ User facing label for the template """

    blocked: bool = models.BooleanField(default=False)
    """ Wether the allow users interacting with the template """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ The date the template was added into the database. """
        
    app_name: str = models.CharField(max_length=128, blank=True, null=True)
    """ For linking to a django application """
    
    extid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="Automatically generated id for external identification of the template",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically generated id for external identification of the template. """
    
    class Meta:
        verbose_name = "template"
        verbose_name_plural = "templates"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['app_name',]),
        ]

    def __str__(self):
        return f"{self.name}" 


class Service(models.Model):
    """Service model keeps track of an instance of a service that can be deployed in a region"""

    name: str = models.CharField(max_length=128)
    """ User facing label for the service """

    blocked: bool = models.BooleanField(default=False)
    """ Wether the allow users interacting with the service """
    
    extid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="Automatically generated id for external identification of the service",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically generated id for external identification of the service. """

    pid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="UUID for tracking of this service on the deployment platform",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ An automatically generated unique ID used to identify services on clouds. """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ The date the service was added into the database. """

    region: Region = models.ForeignKey(Region, related_name="services", on_delete=models.CASCADE)
    """ Region where the service is deployed """
    
    org: Org = models.ForeignKey(Org, related_name="services", on_delete=models.CASCADE)
    """ Org where the service is owned """
    
    app_name: str = models.CharField(max_length=128, blank=True, null=True)
    """ The name of the django application linked to this service """
    
    status: str = models.CharField(max_length=150, choices=ServiceStatus.choices, default=ServiceStatus.NEW)
    """ The current status of the service """
    
    template: Template = models.ForeignKey(Template, related_name="services", on_delete=models.CASCADE)
    """ The template used to create this service """
    
    template_version: str = models.CharField(max_length=128, blank=True, null=True)
    """ The version of the template used to create this service """
    
    settings = models.JSONField(default=dict)
    """ The settings used to create this service """
    
    node: str = models.CharField(max_length=128, blank=True, null=True)
    """ The node where the service is deployed """

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['pid',]),
        ]

    def __str__(self):
        return f"{self.name}"    
    
    def get_controller(self) -> IServiceController:
        """ Get the controller for this service """
        model_path = settings.SERVICE_CONTROLLER
        module, klass = model_path.rsplit(".", 1)
        services = __import__(module, fromlist=[klass])
        controller = getattr(services, klass)
        return controller(self)