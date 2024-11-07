import datetime
import uuid
from django.db import models


class Region(models.Model):
    """A deployment area, section or group for services"""

    name: str = models.CharField(max_length=256, unique=True)
    """ Unique ID for this region """

    created: datetime = models.DateTimeField(editable=False, auto_now_add=True)
    """ Creation date """

    disabled: bool = models.BooleanField()
    """ Wether to disable selecting this region for services """

    templateFilter = models.ManyToManyField('Template', help_text="Sites that can display this template.")
    """ A filter to only allow certain types of templates to run in this region """

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class Service(models.Model):
    """
    A service ...
    """

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

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['extid',]),
            models.Index(fields=['pid',]),
        ]

    def __str__(self):
        # TemplateSKU.objects.filter()
        return f"{self.name}"