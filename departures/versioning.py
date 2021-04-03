from rest_framework.versioning import AcceptHeaderVersioning

class DeparturesAPIVersioning(AcceptHeaderVersioning):
    default_version = '1.0'
    allowed_versions = ('1.0', '2.0')
    version_param = 'version'
