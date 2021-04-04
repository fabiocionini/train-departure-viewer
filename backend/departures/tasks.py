from celery import shared_task
from celery.signals import worker_ready

@shared_task
def update_stations(**kwargs):
    print('Update stations')

@shared_task
def update_departures(**kwargs):
    print('Update departures')

@worker_ready.connect()
def update_all(**kwargs):
    print('Update all')
    update_stations()
    update_departures()
