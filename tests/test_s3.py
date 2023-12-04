from django.test import TestCase

from django_storage_url import get_storage
from django_storage_url.backends.s3 import S3Storage


class S3BackendTestCase(TestCase):
    def test_get_s3_storage(self):
        storage = get_storage(
            "s3://"
            "access_key_id:secret_access_key@"
            "bucket.example.com.s3.amazonaws.com"
            "/?auth=s3v4&domain=custom.com"
        )

        self.assertIsInstance(storage, S3Storage)

        self.assertEqual(storage.access_key, "access_key_id")
        self.assertEqual(storage.secret_key, "secret_access_key")
        self.assertEqual(storage.bucket_name, "bucket.example.com")
        self.assertEqual(storage.endpoint_url, "https://s3.amazonaws.com/")
        self.assertEqual(storage.addressing_style, "path")
        self.assertEqual(storage.signature_version, "s3v4")
        self.assertEqual(storage.location, "")
        self.assertEqual(storage.region_name, None)
        self.assertEqual(storage.custom_domain, "custom.com")
        self.assertEqual(storage.object_parameters, {"ACL": "public-read"})
        self.assertEqual(storage.querystring_auth, False)
        self.assertEqual(storage.url_protocol, "https:")
        self.assertEqual(storage.base_url, "https://custom.com/")

    def test_get_s3_storage_regional(self):
        storage = get_storage(
            "s3://"
            "access_key_id:secret_access_key@"
            "bucket.example.com.s3.eu-west-1.amazonaws.com"
        )

        self.assertEqual(storage.bucket_name, "bucket.example.com")
        self.assertEqual(storage.endpoint_url, "https://s3.eu-west-1.amazonaws.com/")
        self.assertEqual(storage.region_name, "eu-west-1")

    def test_get_s3_storage_regional_fips_dualstack(self):
        storage = get_storage(
            "s3://"
            "access_key_id:secret_access_key@"
            "bucket.example.com.s3-fips.dualstack.eu-west-1.amazonaws.com"
        )

        self.assertEqual(storage.bucket_name, "bucket.example.com")
        self.assertEqual(
            storage.endpoint_url,
            "https://s3-fips.dualstack.eu-west-1.amazonaws.com/",
        )
        self.assertEqual(storage.region_name, "eu-west-1")

    def test_get_s3_storage_regional_deprecated(self):
        storage = get_storage(
            "s3://"
            "access_key_id:secret_access_key@"
            "bucket.example.com.s3-eu-west-1.amazonaws.com"
        )

        self.assertEqual(storage.bucket_name, "bucket.example.com")
        self.assertEqual(storage.endpoint_url, "https://s3-eu-west-1.amazonaws.com/")
        self.assertEqual(storage.region_name, "eu-west-1")
