import six

from django.core.files.storage import (
    FileSystemStorage as DjangoFileSystemStorage,
)


class FileSystemStorage(DjangoFileSystemStorage):
    def __init__(self, dsn):
        base_url = dsn.args.get("url")
        super(FileSystemStorage, self).__init__(
            location=six.text_type(dsn.path), base_url=base_url
        )
        if base_url is None:
            self.base_url = None
