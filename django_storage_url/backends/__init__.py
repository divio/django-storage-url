from django.core.files.storage import (
    get_storage_class as django_get_storage_class,
)


SCHEMES = {
    "az": "django_storage_url.backends.az.AzureStorage",
    "file": "django_storage_url.backends.file.FileSystemStorage",
    "s3": "django_storage_url.backends.s3.S3Storage",
}


def register_storage_class(scheme, backend_path):
    SCHEMES[scheme] = backend_path


def get_storage_class(scheme):
    return django_get_storage_class(SCHEMES[scheme])
