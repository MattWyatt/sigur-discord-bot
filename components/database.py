import os
import sqlite3
from components import component


class Database(component.Component):
    def __init__(self, in_memory=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.in_memory = in_memory

        if self.in_memory:
            self.connection = sqlite3.connect(":memory:", check_same_thread=False)
            self.file_path = ":memory:"
        else:
            self.file_path = "./{}.db".format(self.name)
            if not os.path.exists(self.file_path):
                db = open(self.file_path, "w+")
                db.close()
                self.logger.debug("created database file {}".format(self.file_path))
            self.connection = sqlite3.connect(self.file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    # function run without user input
    def make_table(self, table_name, table_schema):
        sql_schema = ""
        for key in table_schema:
            sql_schema += "{} {}, ".format(key, table_schema[key], "{}")
        sql_schema = sql_schema[:-2]
        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, sql_schema)
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_table(self, table_name):
        sql = "DROP TABLE {}".format(table_name)
        self.cursor.execute(sql)
        self.connection.commit()

    def table_exists(self, table_name):
        sql = "SELECT * FROM sqlite_master"
        self.cursor.execute(sql)
        for table in self.cursor.fetchall():
            if table[2] == table_name:
                return True
        return False

    # function possibly run with user input
    def insert_into_table(self, table_name, *args):
        placeholders = "?," * len(args)
        sql = "INSERT INTO {} VALUES ({})".format(table_name, placeholders)
        # remove last comma and convert args to tuple
        self.cursor.execute(sql[:-2]+")", tuple(args))
        self.connection.commit()

    def delete_from_table(self, table_name, key, value):
        sql = "DELETE FROM {} WHERE {}=?".format(table_name, key)
        self.cursor.execute(sql, (value,))
        self.connection.commit()

    # function possibly run with user input
    def retrieve_from_table(self, table_name, key, value, amount=0):
        sql = "SELECT * FROM {} WHERE {}=?".format(table_name, key)
        self.cursor.execute(sql, (value,))
        self.connection.commit()
        if amount != 0:
            return self.cursor.fetchmany(amount)
        return self.cursor.fetchall()

    def retrieve_all_from_table(self, table_name):
        sql = "SELECT * FROM {}".format(table_name)
        self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.fetchall()

