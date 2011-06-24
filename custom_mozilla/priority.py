from app.utils import safe_string, log

from error.signals import error_created

def priority(instance, **kw):
    log("Firing signal: priority")
    if instance.type in ['OperationalError', 'SMTPRecipientsRefused']:
        instance.priority = 7
        instance.save()
   
    project_url = instance.group.project_url
    if project_url:
        stage = project_url.stage
        log("Firing signal: priority, %s" % stage)
        if stage == 'production':
            instance.priority -= 2
        elif stage == 'testing':
            instance.priority += 2

    instance.priority = max(instance.priority, 1)
    instance.priority = min(instance.priority, 10)
    instance.save()

error_created.connect(priority, dispatch_uid='change_priority')
