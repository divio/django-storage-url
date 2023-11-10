import pickle

from django.test import TestCase, override_settings
from django.db.migrations.serializer import serializer_factory

from django_storage_url import dsn_configured_storage


class DeconstructTestCase(TestCase):
    @override_settings(STORAGE_DSN="file:///test/media")
    def test_generated_class_module(self):
        storage = dsn_configured_storage("STORAGE_DSN")
        storage._setup()  # Storage is a LazyObject, make sure it is set up
        self.assertEqual(
            storage._wrapped.__module__, "django_storage_url.backends.file"
        )
        self.assertEqual(
            storage._wrapped.__class__.__module__,
            "django_storage_url.backends.file",
        )

    def test_not_implemented_deconstructible(self):
        storage = dsn_configured_storage("UNDEFINED_DSN")

        arg_string, arg_imports = serializer_factory(storage).serialize()
        self.assertEqual(
            arg_string,
            "django_storage_url.base.dsn_configured_storage('UNDEFINED_DSN')",
        )
        self.assertEqual(arg_imports, {"import django_storage_url.base"})

    @override_settings(STORAGE_DSN="file:///test/media")
    def test_defined_deconstructible(self):
        storage = dsn_configured_storage("STORAGE_DSN")

        arg_string, arg_imports = serializer_factory(storage).serialize()
        self.assertEqual(
            arg_string,
            "django_storage_url.base.dsn_configured_storage('STORAGE_DSN')",
        )
        self.assertEqual(arg_imports, {"import django_storage_url.base"})


class PickleTestCase(TestCase):
    @override_settings(STORAGE_DSN="file:///test/media")
    def test_pickle_lazy(self):
        storage = dsn_configured_storage("STORAGE_DSN")

        dumped = pickle.dumps(storage)
        loaded = pickle.loads(dumped)

        # Make sure that once unpickled it's still referring to the same object
        storage._setup()
        loaded._setup()

        assert loaded._wrapped.__dict__ == storage._wrapped.__dict__
        assert loaded._wrapped.__module__ == storage._wrapped.__module__
        assert loaded._wrapped.__class__.__name__ == storage._wrapped.__class__.__name__
        assert (
            loaded._wrapped.__class__.__bases__ == storage._wrapped.__class__.__bases__
        )

    @override_settings(STORAGE_DSN="file:///test/media")
    def test_pickle_wrapped(self):
        storage = dsn_configured_storage("STORAGE_DSN")
        storage._setup()

        dumped = pickle.dumps(storage)
        loaded = pickle.loads(dumped)

        # Make sure that once unpickled it's still referring to the same object
        loaded._setup()

        assert loaded._wrapped.__dict__ == storage._wrapped.__dict__
        assert loaded._wrapped.__module__ == storage._wrapped.__module__
        assert loaded._wrapped.__class__.__name__ == storage._wrapped.__class__.__name__
        assert (
            loaded._wrapped.__class__.__bases__ == storage._wrapped.__class__.__bases__
        )
