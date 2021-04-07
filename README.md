# train-departure-viewer
Test assignment - A view depicting all train departures in any direction for a station ‘Den Haag Centraal’

## Requirements

This is a multi-containerized application that runs on Docker, therefore Docker desktop or server version must be installed.


## Installation

The file .env.sample contained in the root directory of the project can be used to create a .env to provide the necessary environment variables.
**Warning**: for demonstration purposes and to be able to give a working environment "out of the box" there is already a .env file with the correct values.

```
docker-compose build
```
Will build the backend and the frontend.

```
docker-compose up
```
Will bring up the applications.

The frontend will be then available at http://localhost:8080

Optionally you can generate a super-user to access the Django admin panel. 
Reach the shell for the backend app through the Docker dashboard (or via command line) and then: 

```
cd /opt/app/backend
pipenv shell
python manage.py createsuperuser
```

## Application details

### Backend

The backend uses latest version of Django together with several application modules:
- REST Framework
- REST Framework Api Key
- Celery integration

The database engine is PostgreSQL for the production environment and SQLite for the development environment.
The REST API uses both user/password authentication + JWT and api key authorization.
**Warning**: for demonstration purposes and to be able to give a working environment "out of the box", the REST API GET methods are accessible also without authorization. The backend has functioning api key and JWT based authorization setup, it is just currently "bypassed".

The API access is throttled for anonymous and authorized access. The settings are configurable in the Django settings.

API is versioned through the use of Accept header, passing a custom mime-type and the version (currently 1.0 or 2.0), i.e.:
```
Accept: application/vnd.fabiocionini.departures+json; version=1.0
```

The GET responses are cached through the ETag server header, matched by the If-None-Match client header. This caching system is transparently handled by the browser.

### Celery scheduled updaters
The updates from the train provider service are handled by a Celery Beat schedule that is integrated with Django and runs periodical scripts to update the departures and the station code.


### Frontend

The frontend is developed in Angular 11 and ng-Bootstrap 4.0.
The application is built in production mode (AOT) by a multi-stage Docker script. 
This single page application provides a train departure panel layout which shows 10 departures at a time, switching page every 10 seconds. The trains are ordered by ascending departure date. The trains that are about to leave (in 5 minutes) will show an animated "boarding" dot on the right.
The application retrieves data from the Django REST API every 10 seconds (although the cache mechanism minimizes the network traffic).
All application settings are configurable through the src/environments files (API url, data refresh rate, page cycle rate, boarding time, number of departures per page).
The view has been developed with responsiveness in mind (rem-based sizes, responsive table).

**Room for improvement**: although the application has been developed with SSR compatibility in mind, it does not currently implement Server Side Rendering.


### Server setup
An Nginx proxy handles the incoming connections, functioning as a reverse proxy for the Django backend (which is served through Gunicorn) and also serving static pages (the frontend application and its assets).


