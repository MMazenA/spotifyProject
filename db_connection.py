"""Database connection singleton."""
from multiprocessing import Lock
import threading
import mysql.connector.pooling


class Singleton(type):
    """Singleton metaclass to build from."""

    def __new__(mcs, name, bases, attrs):
        # Assume the target class is created (i.e. this method to be called) in the main thread.
        cls = super(Singleton, mcs).__new__(mcs, name, bases, attrs)
        cls.__shared_instance_lock__ = Lock()
        return cls

    def __call__(cls, *args, **kwargs):
        with cls.__shared_instance_lock__:
            try:
                return cls.__shared_instance__
            except AttributeError:
                cls.__shared_instance__ = super(Singleton, cls).__call__(
                    *args, **kwargs
                )
                return cls.__shared_instance__


class DBC(metaclass=Singleton):
    """Uses singleton to create DBC class object."""

    _thread_local = threading.local()

    def __init__(self, **kwargs) -> None:
        try:
            db_config = {
                "host": kwargs["host"],
                "user": kwargs["user"],
                "password": kwargs["password"],
                "database": kwargs["database"],
                "connection_timeout": kwargs["connection_timeout"],
            }
            self._mydb = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="db_pool", pool_size=15, **db_config
            )

        except mysql.connector.Error as sqlerr:
            print("Unable to connect to database: ", sqlerr)

    @property
    def connection(self):
        """Returns thread-local database connection or creates one"""
        if not hasattr(self._thread_local, "connection"):
            self._thread_local.connection = self._mydb.get_connection()
        return self._thread_local.connection

    def release_connection(self):
        """Releases thread-local database connection"""
        if hasattr(self._thread_local, "connection"):
            self._thread_local.connection.close()
            del self._thread_local.connection

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.release_connection()
