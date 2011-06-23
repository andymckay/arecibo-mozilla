from app.utils import safe_string, log

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from error import signals
from error.signals import error_created
from error.listeners import default_grouping
from error.models import Error, Group

error_created.disconnect(default_grouping, dispatch_uid="default_grouping")


def generate_key(instance):
    keys = ["type", "msg", "status", "domain"]
    hsh = None

    for key in keys:
        value = safe_string(getattr(instance, key))
        if value:
            if not hsh:
                hsh = md5()
            hsh.update(value.encode("ascii", "ignore"))

    return hsh

def default_grouping(instance, **kw):
    """ Given an error, see if we can fingerprint it and find similar ones """
    log("Firing signal: default_grouping")

    hsh = generate_key(instance)
    if hsh:
        digest = hsh.hexdigest()
        try:
            created = False
            group = Group.objects.filter(uid=digest)[0]
            group.count = Error.objects.filter(group=group).count() + 1
            group.save()
        except IndexError:
            created = True
            group = Group()
            group.uid = digest
            group.count = 1
            group.save()

        instance.group = group
        instance.save()

        if created:
            signals.group_assigned.send(sender=group.__class__, instance=group)

signals.error_created.connect(default_grouping,
                              dispatch_uid="default_grouping")
