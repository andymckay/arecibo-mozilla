from app.utils import log
from notifications.models import Notification
from django.contrib.auth.models import User

from projects.models import Project
from error.signals import error_created

amo_users = ['amo-tracebacks@mozilla.org']
amo_domains = ['addons-dev.allizom.org', 'addons.allizom.org', 'addons.mozilla.org',
               'apps-preview-dev.allizom.org', 'apps-preview.allizom.org', 'apps-preview.mozilla.org',
               'marketplace-dev.allizom.org', 'marketplace.allizom.org', 'marketplace.mozilla.org']


def amo_notification(instance, **kw):
    """ Given an error see if we need to send a notification """
    log('Firing signal: default_notification')

    user = User.objects.get(email__in=amo_users)
    if instance.domain in amo_domains:
        notification = Notification()
        notification.notifier = instance
        notification.save()
    notification.user.add(user)


error_created.connect(amo_notification, dispatch_uid='amo_notification')
