"""Database connection singleton."""
from multiprocessing import Lock
import mysql.connector
import privateinfo

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
                cls.__shared_instance__ = super(Singleton, cls).__call__(*args, **kwargs)
                return cls.__shared_instance__

class DBC(metaclass=Singleton):
    """Uses singleton to create DBC class object."""
    def __init__(self, **kwargs) -> None:
        try:
            self._mydb = mysql.connector.connect(
                    host=kwargs["host"],
                    user=kwargs["user"],
                    password=kwargs["password"],
                    database=kwargs["database"],
                    connection_timeout=kwargs["connection_timeout"],
                )
        except mysql.connector.Error as sqlerr:
            print("Unable to connect to database: ", sqlerr)

    def get_connection(self) -> mysql.connector.connect: 
        """Returns database connection or makes one"""
        return self._mydb

    def __del__(self) -> None:
        """Closing database connection."""
        if self._mydb is not None:
            self._mydb.close()

# def static_init(cls) -> None:
#         if getattr(cls, "static_init", None):
#             DBC(host=privateinfo.sql_host(),
#                     user=privateinfo.sql_user(),
#                     password=privateinfo.sql_pass(),
#                     database=privateinfo.sql_db(),
#                     connection_timeout=5,).get_connection()   
#             cls.static_init()
#         return cls

# @static_init
# class SQL():
#     """SQL queries handler."""

#     DBC(host=privateinfo.sql_host(),
#                     user=privateinfo.sql_user(),
#                     password=privateinfo.sql_pass(),
#                     database=privateinfo.sql_db(),
#                     connection_timeout=5,).get_connection()       


# # DBC(host=privateinfo.sql_host(),
# #                     user=privateinfo.sql_user(),
# #                     password=privateinfo.sql_pass(),
# #                     database=privateinfo.sql_db(),
# #                     connection_timeout=5,).get_connection()