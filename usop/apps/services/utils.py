
from django.conf import settings

_default_service_controller = None
_default_region = None

def get_default_servicecontroller():
    """ Get the default service controller for the current deployment """
    if _default_service_controller is not None:
        return _default_service_controller    
    model_path = settings.SERVICE_CONTROLLER
    module, klass = model_path.rsplit(".", 1)
    services = __import__(module, fromlist=[klass])
    _default_service_controller = getattr(services, klass)
    return _default_service_controller