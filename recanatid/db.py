import sqlite3
from .config import DEFAULT_DATABASE


def get_db():
    return sqlite3.connect(DEFAULT_DATABASE)
