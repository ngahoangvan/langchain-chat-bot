from celery.app import Celery
from celery.schedules import crontab
from configs.common_config import settings


celery_app = Celery(
    '__background_job__',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@celery_app.task
def test(arg):
    print(arg)


@celery_app.task
def add(x, y):
    z = x + y
    print(z)


# celery_app.conf.beat_schedule = {
#     'add-every-10-seconds': {
#         'task': 'celery_task.celery_app.add',
#         'schedule': 10,
#         'args': (16, 16)
#     },
# }
celery_app.conf.timezone = 'UTC'
