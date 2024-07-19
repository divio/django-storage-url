import base64
from urllib.parse import parse_qs

import furl
from storages.backends import azure_storage
from django.conf import settings


class AzureStorageFile(azure_storage.AzureStorageFile):
    def __init__(self, name, mode, storage):
        super().__init__(name, mode, storage)
        if "w" not in mode:
            # Force early RAII-style exception if object does not exist
            if not storage.exists(name):
                raise IOError("File does not exist: %s" % name)


class AzureStorage(azure_storage.AzureStorage):
    mimetype_overrides = {
        ("application/x-tar", "gzip"): ("application/x-gtar", None),
    }

    def __init__(self, dsn):
        account_name = dsn.username
        credential = dsn.password
        credential += "=" * (-len(credential) % 4)

        if "url" in dsn.args:
            base_url = furl.furl(dsn.args.get("url"))
            secure_urls = base_url.scheme == "https"
            custom_domain = base_url.netloc
        else:
            secure_urls = True
            custom_domain = dsn.args.get("domain")
            base_url = furl.furl()
            base_url.scheme = "https"
            base_url.host = custom_domain or "{}.{}".format(account_name, dsn.host)

        container_name = str(dsn.path).strip("/")
        base_url.path = container_name + "/"

        super().__init__()
        self.account_name = account_name
        try:
            # SAS token
            sas_token = base64.b64decode(credential).decode("ascii")
        except UnicodeDecodeError:
            # Account key (binary data)
            self.account_key = credential
        else:
            if "sig" in parse_qs(sas_token):
                self.sas_token = sas_token
            else:
                # Account key (ascii)
                self.account_key = credential

        self.azure_container = container_name
        self.azure_ssl = secure_urls
        self.max_memory_size = 10 * 1024**2
        # The default is False in the superclass
        self.overwrite_files = getattr(settings, "AZURE_OVERWRITE_FILES", True)
        self.location = ""
        self.base_url = str(base_url)

    def url(self, name, expire=None, reset_query=True):
        url = super().url(name, expire)
        url = furl.furl(url)
        # TODO: How does this work when using a custom url
        #       with an additional domain?
        url.netloc = furl.furl(self.base_url).netloc

        if reset_query:
            # By default, reset the query parameters to remove SAS tokens from the URL.
            url.query = ""
        return str(url)

    def _open(self, name, mode="rb"):
        return AzureStorageFile(name, mode, self)

    def _get_content_settings_parameters(self, name, content=None):
        # Azure forwards the Content-Encoding header set during upload to
        # download request responses (causing transparent decompression by most
        # clients when it is set to ``gzip``).
        # The superclass uses the return value of ``mimetypes.guess_type``,
        # which is explicitly documented as not suitable for
        # content *transfer* encoding.
        #
        # NOTE: The content-encoding header should probably *never* be set by
        #       this storage backend.
        #
        # https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
        #
        params = super()._get_content_settings_parameters(name, content=content)
        type_enc = (params["content_type"], params["content_encoding"])
        (
            params["content_type"],
            params["content_encoding"],
        ) = self.mimetype_overrides.get(type_enc, type_enc)
        return params
