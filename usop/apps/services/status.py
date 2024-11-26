from django.utils.translation import gettext_lazy as _

from django.db.models import TextChoices


class ServiceStatus(TextChoices):
   NEW  = 'NEW', _('New')
   """ The service is new and has not been deployed """

   DEPLOYING = 'DEPLOYING', _('Deploying')
   """ The service is being deployed in target region """
   
   DEPLOYING_FAILED = 'DEPLOYING_FAILED', _('Deploying failed')
   """ The service deployment failed """

   RUNNING = 'RUNNING', _('Running')
   """ The service is currently running """

   STOPPING = 'STOPPING', _('Stopping')
   """ The service is being stopped """

   STOPPED = 'STOPPED', _('Stopped')
   """ The service has been stopped and is not utilizing CPU or memory. Storage is still being used. """
   
   TO_UPGRADE = 'TO_UPGRADE', _('To upgrade')
   """ The service is runnign but is marked for an upgrade in the chart """
   
   UPGRADING = 'UPGRADING', _('Upgrading')
   """ The service is being upgraded """
   
   UPGRADING_FAILED = 'UPGRADING_FAILED', _('Upgrading failed')
   """ The service upgrade failed """

   RESUMMING = 'RESUMMING', _('Resumming')
   """ The service is being resumed from a stopped state """

   CLEARING = 'CLEARING', _('Clearing')
   """ The service is being cleared from the platform """

   DESTROYED = 'DESTROYED', _('Destroyed')
   """ The service has been cleared from the platform """

   BACKING_UP = 'BACKING_UP', _('Backing up')
   """ The service storage resources are being backed up. Services are still running. """