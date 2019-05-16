from django.core.files.storage import Storage
from .signals import transaction_signals
from .tasks import delete_file


class DelayHook(Storage):
    def __init__(self, storage):
        self.storage = storage
        self.reset()
        signal_processor(self)

    def __nonzero__(self):
        return bool(self.storage)

    def __str__(self):
        return str(self.storage)

    def __repr__(self):
        return repr(self.storage)

    def reset(self):
        self.delete_on_commit = []
        self.delete_on_rollback = []

    def delete(self, name):
        self.delete_on_commit.append(name)

    def delete_instantly(self, name):
        return self.storage.delete(name)

    def rename(self, old_file, new_filename, rewrite=False):
        old_filename = old_file.name
        if rewrite:
            self.delete_instantly(new_filename)
        else:
            new_filename = self.storage.get_available_name(new_filename)
        old_file.save(new_filename, old_file)
        self.storage.delete(old_filename)

    def _save(self, name, content):
        self.delete_on_rollback.append(name)
        return self.storage.save(name, content)

    def _open(self, name, mode):
        return self.storage.open(name, mode)

    def exists(self, name):
        return self.storage.exists(name)

    def size(self, name):
        return self.storage.size(name)

    def get_avaiable_name(self, name):
        return self.storage.get_avaiable_name(name)

    def get_valid_name(self, name):
        return self.storage.get_valid_name(name)

    def listdir(self, path):
        return self.storage.listdir(path)

    def url(self, name):
        return self.storage.url(name)

    def on_commit(self):
        for f in self.delete_on_commit:
            delete_file.delay(self.storage, f)
        self.reset()

    def on_rollback(self):
        for f in self.delete_on_rollback:
            delete_file.delay(self.storage, f)
        self.reset()


def signal_processor(storage):
    def on_commit(signal, **kwargs):
        storage.on_commit()

    def on_rollback(signal, **kwargs):
        storage.on_rollback()

    transaction_signals.post_commit.connect(on_commit, weak=False)
    transaction_signals.post_rollback.connect(on_rollback, weak=False)
