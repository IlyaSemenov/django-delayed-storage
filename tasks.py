from celery import task
#from djcelery_transactions import task


@task(name='delete_file')
def delete_file(storage, filename):
    storage.delete(filename)

