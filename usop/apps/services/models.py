import datetime
import uuid
from django.db import models
from django.conf import settings

from .allocation import DefaultNodeAllocator, NodeAllocator
from .status import ServiceStatus
from usop.apps.users.models import Org
from .interfaces import *
from usop.lib.CachedClassUtil import CachedClassUtil




class Region(models.Model):
    """A deployment area, section or group for services"""

    name: str = models.CharField(max_length=256, unique=True)
    """ Unique ID for this region """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ Creation date """

    disabled: bool = models.BooleanField()
    """ Wether to disable selecting this region for services """
    
    namespace: str = models.CharField(max_length=128, blank=True, null=True)
    """ Optional kubernetes namespace used for this region, leaving blank will use the default namespace """

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
    def get_node_allocator(self) -> NodeAllocator:
        return DefaultNodeAllocator()


class Template(models.Model):
    """ 
        A template is a base configuration for a service that can be deployed.
    """

    name: str = models.CharField(max_length=128)
    """ User facing label for the template """

    extid = models.UUIDField(
        verbose_name="Ext ID",
        help_text="Automatically generated id for external identification of the template",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically generated id for external identification of the template. """

    pid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="UUID for tracking of this template on the deployment platform",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ An automatically generated unique ID used to identify templates on clouds. """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ The date the template was added into the database. """
    
    template_settings = models.JSONField(blank=True, null=True)
    """ Default helm settings for this template sku """
    
    chart_id: str = models.CharField(max_length=256)
    """ The Helm chart ID for this template """
    
    class Meta:
        verbose_name = "template"
        verbose_name_plural = "templates"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['pid',]),
        ]

    def __str__(self):
        return f"{self.name}"
    
    def get_controller(self) -> IServiceController:
        """ Get the controller for this template """
        model_path = settings.SERVICE_CONTROLLER
        module, klass = model_path.rsplit(".", 1)
        services = __import__(module, fromlist=[klass])
        controller = getattr(services, klass)
        return controller(self)


class TemplateSKU(models.Model):
    """ 
        A SKU is a specific version of a template that can be deployed.
        This allows for multiple variations of templates.
    """
    
    template: Template = models.ForeignKey(Template, related_name="skus", on_delete=models.CASCADE)
    """ Template this SKU is for """
    
    name: str = models.CharField(max_length=256)
    """ User facing label for the SKU """    
    
    description: str = models.TextField(blank=True, null=True)
    """ Description of the SKU """

    region: Region = models.ForeignKey(Region, related_name="templates", on_delete=models.CASCADE)
    """ Region where the template can be deployed, if not set, it can be deployed in all regions """
    
    org: Org = models.ForeignKey(Org, related_name="templates", on_delete=models.CASCADE)
    """ Org where the template can be used, if not set, it can be used by all orgs """    
    
    ui_enabled: bool = models.BooleanField(default=True)
    """ Wether the template can be used in UIs """    
    
    extid = models.UUIDField(
        verbose_name="Ext ID",
        help_text="Automatically generated id for external identification of the template sku",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically generated id for external identification of the template sku. """
    
    pid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="UUID for tracking of this template sku on the deployment platform",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ An automatically generated unique ID used to identify template skus on clouds. """
    
    sku_settings = models.JSONField(blank=True, null=True)
    """ Default helm settings for this template sku """
    
    class Meta:
        verbose_name = "template sku"
        verbose_name_plural = "template skus"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['pid',]),
        ]

    def __str__(self):
        return f"{self.name}"


class TemplateVersion(models.Model):
    """A version of a template for deploying services"""

    version_name: str = models.CharField(max_length=128)
    """ User facing label for the template version """
    
    template: Template = models.ForeignKey(Template, related_name="versions", on_delete=models.CASCADE)
    """ Template this version is for """

    helm_repo: str = models.CharField(max_length=256)
    """ The Helm repository URL for this template version """

    extid = models.UUIDField(
        verbose_name="Ext ID",
        help_text="Automatically generated id for external identification of the template version",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ Automatically generated id for external identification of the template version. """

    pid = models.UUIDField(
        verbose_name="Platform ID",
        help_text="UUID for tracking of this template version on the deployment platform",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    """ An automatically generated unique ID used to identify template versions on clouds. """
    
    version_settings = models.JSONField(blank=True, null=True)
    """ Default helm settings for this template version """

    class Meta:
        verbose_name = "template version"
        verbose_name_plural = "template versions"
        ordering = ["version_name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['pid',]),
        ]

    def __str__(self):
        return f"{self.version_name}"


class Service(models.Model):
    """Service model keeps track of an instance of a service that can be deployed in a region"""

    name: str = models.CharField(max_length=128)
    """ User facing label for the service """

    blocked: bool = models.BooleanField(default=False)
    """ Wether the allow users interacting with the service """
    
    extid = models.UUIDField(
        verbose_name="Ext ID",
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
    
    template_sku: TemplateSKU = models.ForeignKey(TemplateSKU, related_name="services", on_delete=models.CASCADE, blank=True, null=True)
    """ Optional template sku used to deploy this service """
    
    template_version: TemplateVersion = models.ForeignKey(TemplateVersion, related_name="services", on_delete=models.CASCADE, blank=True, null=True)
    """ The template version used to deploy this service """
    
    settings = models.JSONField(blank=True, null=True)
    """ Helm settings for this template version """

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
    
    def get_service_controller(self) -> IServiceController:
        """ Get the controller for this service """
        model_path = settings.SERVICE_CONTROLLER
        # TODO allow apps to define their own controllers
        _class = CachedClassUtil.get_class(model_path)
        return _class(self)
    
    @property
    def namespace(self):
        return self.service.region.namespace or settings.DEFAULT_NAMESPACE
    
    @property
    def get_billing_controller(self) -> IBillingController:
        """ Get the billing controller for this service """
        model_path = settings.BILLING_CONTROLLER
        # TODO allow apps to define their own controllers
        return CachedClassUtil.get_instance(model_path)