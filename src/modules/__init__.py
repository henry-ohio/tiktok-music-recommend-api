from .sql_database_module import *
from kink import di

di[AsyncEngine] = lambda di: connect_database()