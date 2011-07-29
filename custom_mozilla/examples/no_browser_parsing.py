from notifications.listeners import default_browser_parsing
from error.signals import error_created

error_created.disconnect(default_browser_parsing,
                         dispatch_uid="default_browser_parsing")

