from rest_framework.renderers import JSONRenderer


class DeparturesAPIRenderer(JSONRenderer):
    media_type = 'application/vnd.fabiocionini.departures+json'
