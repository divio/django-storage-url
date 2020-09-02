import base64

import furl
from azure.storage.blob.models import PublicAccess
from storages.backends import azure_storage


class AzureStorageFile(azure_storage.AzureStorageFile):
    def __init__(self, name, mode, storage):
        super().__init__(name, mode, storage)
        if "w" not in mode:
            # Force early RAII-style exception if object does not exist
            if not storage.exists(name):
                raise IOError("File does not exist: %s" % name)


class AzureStorage(azure_storage.AzureStorage):
    def __init__(self, dsn):
        account_name = dsn.username
        sas_token = dsn.password
        sas_token += "=" * (-len(sas_token) % 4)
        sas_token = base64.b64decode(sas_token).decode("ascii")

        if "url" in dsn.args:
            base_url = furl.furl(dsn.args.get("url"))
            secure_urls = base_url.scheme == "https"
            custom_domain = base_url.netloc
        else:
            secure_urls = True
            custom_domain = dsn.args.get("domain")
            base_url = furl.furl()
            base_url.scheme = "https"
            base_url.host = custom_domain or "{}.{}".format(
                account_name, dsn.host
            )

        # TODO: Make the default `private` and explicitly set the ACL to
        #       `public-read` during provisioning
        acl = dsn.args.get("acl", "public-read")
        container_name = str(dsn.path).strip("/") or "public-media"
        base_url.path = container_name + "/"

        super().__init__()
        self.account_name = account_name
        self.account_key = None
        self.sas_token = sas_token
        self.azure_container = container_name
        self.azure_ssl = secure_urls
        self.max_memory_size = 10 * 1024 ** 2
        self.overwrite_files = True
        self.location = ""
        self.base_url = str(base_url)

        self.ensure_container_exists(acl)

    def url(self, name, expire=None):
        url = super().url(name, expire)
        url = furl.furl(url)
        # TODO: How does this work when using a custom url
        #       with an additional domain?
        url.netloc = furl.furl(self.base_url).netloc
        return str(url)

    def ensure_container_exists(self, acl):
        public_access = PublicAccess.Blob if acl == "public-read" else None
        # TODO: If it exists, ensure that the ACL matches
        self.service.create_container(
            self.azure_container,
            public_access=public_access,
            fail_on_exist=False,
        )

    def _open(self, name, mode="rb"):
        return AzureStorageFile(name, mode, self)
