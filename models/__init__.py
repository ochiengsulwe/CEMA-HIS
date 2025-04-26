"""
initialize the models package
"""

from os import getenv


storage_t = getenv("CEMA_HIS_TYPE_STORAGE")

if storage_t == "db":
    from .engine.db_storage import DBStorage
    storage = DBStorage()

# storage.reload()
