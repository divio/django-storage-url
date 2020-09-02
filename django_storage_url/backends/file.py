from django.core.files.storage import (
    FileSystemStorage as DjangoFileSystemStorage,
)


class FileSystemStorage(DjangoFileSystemStorage):
    def __init__(self, dsn):
        base_url = dsn.args.get("url")
        super().__init__(location=str(dsn.path), base_url=base_url)
        if base_url is None:
            self.base_url = None
