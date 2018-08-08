import os
import sqlite3
from components import exceptions
from components import component


class Database(component.Component):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_path = "./{}.db".format(self.name)
        if not os.path.exists(self.file_path):
            db = open(self.file_path, "w+")
            db.close()
            self.logger.debug("created database file {}".format(self.file_path))

        self.connection = sqlite3.connect(self.file_path)
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

    def insert_into_table(self, table_name, values):
        sql = "INSERT INTO {} VALUES (?)".format(table_name)
        self.cursor.execute(sql, values)







