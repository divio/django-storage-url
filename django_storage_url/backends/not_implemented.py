from django.core.files.storage import Storage


class NotImplementedStorage(Storage):
    def open(self, name, mode="rb"):
        raise NotImplementedError

    def save(self, name, content, max_length=None):
        raise NotImplementedError

    def get_valid_name(self, name):
        raise NotImplementedError

    def get_available_name(self, name, max_length=None):
        raise NotImplementedError
