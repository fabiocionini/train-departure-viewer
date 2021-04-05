from celery import shared_task
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from django.conf import settings
from departures.models import Station, Departure
import requests

import sys

logger = get_task_logger(__name__)

cfg = settings.DEPARTURES_SETTINGS

def get_default_station():
    station = Station.objects.get(name=cfg['STATION_NAME'])
    if station:
        return station
    return None

def get_headers():
    return {cfg['AUTH_KEY']: cfg['AUTH_VALUE'], 'Accept': 'application/json'}

# def get_train_type(category):
#     return {
#             'SPR': 'Sprinter',
#             'IC': 'Intercity'
#            }.get(category, category)


@shared_task
def update_stations(**kwargs):
    logger.info('Updating stations')
    response = requests.get(cfg['STATIONS_URL'], headers=get_headers(), timeout=(cfg['CONNECT_TIMEOUT'], cfg['READ_TIMEOUT']))
    if response.status_code == 200:
        response_obj = response.json()
        if 'payload' in response_obj:
            station = next((s for s in response_obj['payload'] if s['namen']['lang'] == cfg['STATION_NAME']), None)
            if station:
                try:
                    model, created = Station.objects.update_or_create(name=station['namen']['lang'],
                                                                      defaults={
                                                                         'code': station['code']
                                                                      })
                    if created:
                        logger.info('Station {0} created.'.format(cfg['STATION_NAME']))
                    else:
                        logger.info('Station {0} updated.'.format(cfg['STATION_NAME']))
                except Exception:
                    logger.error('ERROR: {0}'.format(sys.exc_info()))
            else:
                print('Station not found.')
                logger.error('ERROR: Station not found.')
    else:
        logger.error('Connection error: {0}'.format(response.status_code))


@shared_task
def update_departures(**kwargs):
    logger.info('Updating departures')
    station = get_default_station()
    if station:
        headers = {cfg['AUTH_KEY']: cfg['AUTH_VALUE'], 'Accept': 'application/json'}
        response = requests.get(cfg['DEPARTURES_URL'].format(station.code), headers=headers, timeout=(cfg['CONNECT_TIMEOUT'], cfg['READ_TIMEOUT']))
        if response.status_code == 200:
            response_obj = response.json()
            if 'payload' in response_obj:
                if 'departures' in response_obj['payload']:
                    departures = response_obj['payload']['departures']
                    for departure in departures:
                        try:
                            model, created = Departure.objects.update_or_create(name=departure['name'],
                                                                                defaults={
                                                                                    'station': station,
                                                                                    'planned_time': departure['plannedDateTime'],
                                                                                    'direction': departure['direction'],
                                                                                    'platform': departure['plannedTrack'],
                                                                                    'train_type': departure['trainCategory'],
                                                                                })
                            if created:
                                logger.info('Departure {0} created.'.format(departure['name']))
                            else:
                                logger.info('Departure {0} updated.'.format(departure['name']))
                        except Exception:
                            logger.error('ERROR: {0}'.format(sys.exc_info()))
        else:
            logger.error('Connection error: {0}'.format(response.status_code))


@worker_ready.connect()
def update_all(**kwargs):
    logger.info('Update all on worker start.')
    update_stations()
    update_departures()
