# django-delayed-storage

This is a Django storage wrapper that completes the underlying storage operation (such as file upload or deletion) on the database commit hook.

This is useful to prevent the situation when a file has been deleted, but then the database transaction was rolled back. The database will then hold a reference to a file that is already gone.

---

This is an incomplete copy of <https://github.com/pentusha/django-delayed-storage/> which has been deleted and removed from PyPi by the maintainer (my ex-employee).

I restored it from a locally installed egg file.

TODO: republish the package at PyPi.
