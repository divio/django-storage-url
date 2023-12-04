from django.utils.module_loading import import_string


SCHEMES = {
    "az": "django_storage_url.backends.az.AzureStorage",
    "file": "django_storage_url.backends.file.FileSystemStorage",
    "s3": "django_storage_url.backends.s3.S3Storage",
}


def register_storage_class(scheme, backend_path):
    SCHEMES[scheme] = backend_path


def get_storage_class(scheme):
    return import_string(SCHEMES[scheme])
