from django.test import TestCase, override_settings

from django.db.migrations.serializer import serializer_factory

from django_storage_url import dsn_configured_storage


class DeconstructTestCase(TestCase):
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
