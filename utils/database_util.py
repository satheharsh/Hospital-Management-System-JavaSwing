import configparser
import os
import sqlite3

try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

class DatabaseUtil:
    _db_config = None
    _use_sqlite = False
    _sqlite_file = "hospital_db.sqlite"

    @classmethod
    def load_config(cls):
        if cls._db_config is not None:
            return
        
        config = configparser.ConfigParser()
        ini_file = "database.ini"
        if os.path.exists(ini_file):
            config.read(ini_file)
            if "database" in config:
                cls._db_config = dict(config["database"])
        
        if not cls._db_config:
            cls._db_config = {
                "db.host": "localhost",
                "db.port": "3306",
                "db.database": "hospital_db",
                "db.username": "root",
                "db.password": "password"
            }

    @classmethod
    def get_connection(cls):
        cls.load_config()

        if not cls._use_sqlite and HAS_MYSQL:
            try:
                conn = mysql.connector.connect(
                    host=cls._db_config.get("db.host", "localhost"),
                    port=int(cls._db_config.get("db.port", 3306)),
                    user=cls._db_config.get("db.username", "root"),
                    password=cls._db_config.get("db.password", "password"),
                    database=cls._db_config.get("db.database", "hospital_db")
                )
                return conn
            except Exception:
                cls._use_sqlite = True

        conn = sqlite3.connect(cls._sqlite_file)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def execute(cls, cursor, sql: str, params: tuple = ()):
        is_sqlite = False
        try:
            conn = getattr(cursor, 'connection', None)
            if conn and isinstance(conn, sqlite3.Connection):
                is_sqlite = True
            elif type(cursor).__module__.startswith('sqlite3'):
                is_sqlite = True
        except Exception:
            pass

        if is_sqlite or cls._use_sqlite:
            cls._use_sqlite = True
            sql = sql.replace("%s", "?")
            
        cursor.execute(sql, params)

