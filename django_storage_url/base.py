import furl

from django.conf import settings
from django.utils.functional import LazyObject

from .backends import get_storage_class
from .backends.not_implemented import NotImplementedStorage


class _DSNConfiguredStorage(LazyObject):
    def _setup(self):
        dsn = getattr(settings, self._setting_name, None)
        if not dsn:
            self._wrapped = NotImplementedStorage()
        else:
            url = furl.furl(dsn)
            storage_class = get_storage_class(url.scheme)
            # Django >= 1.9 now knows about LazyObject and sets them up before
            # serializing them. To work around this behavior, the storage class
            # itself needs to be deconstructible.
            storage_class = type(
                storage_class.__name__,
                (storage_class,),
                {"deconstruct": self._deconstructor},
            )
            self._wrapped = storage_class(url)


def dsn_configured_storage_class(setting_name):
    path = "{}.{}".format(
        dsn_configured_storage.__module__, dsn_configured_storage.__name__
    )
    return type(
        "DSNConfiguredStorage",
        (_DSNConfiguredStorage,),
        {
            "_setting_name": setting_name,
            "_deconstructor": lambda self: (path, [setting_name], {}),
        },
    )


def dsn_configured_storage(setting_name):
    return dsn_configured_storage_class(setting_name)()


def get_storage(dsn):
    url = furl.furl(dsn)
    storage_class = get_storage_class(url.scheme)
    return storage_class(url)
