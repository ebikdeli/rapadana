import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<project_name>.settings.dev')

app = Celery('<project_name>', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


"""
This is how we must use Celery in the Windows dev environment (in cmd):
    (env)....> celery -A project_name worker -l <INFO> --pool=single
    
and for 'flower' in separate window:
    (env)....> celery -A project_name flower
    
if fact, 'worker' argument run celery workers and 'flower' command run and connect flower process to celery
"""
