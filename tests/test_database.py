import unittest
from components import component
from components import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # dummy component for database to inherit
        c = component.Component()
        c.set_logger("SigurTest")
        c._name = "SigurTest"

        self.db = database.Database(in_memory=True, inherit=c)

        self.table_name = "test_table"
        self.table_schema = {
            "test1": "text",
            "test2": "text"
        }

    def test_make_table(self):
        self.db.make_table(self.table_name, self.table_schema)
        self.assertTrue(self.db.table_exists(self.table_name))

    def test_insert_retrieve(self):
        self.db.make_table(self.table_name, self.table_schema)
        self.db.insert_into_table(self.table_name, "value1", "value2")
        result = self.db.retrieve_from_table(self.table_name,
                                             self.table_schema.__iter__().__next__(),
                                             "value1")
        self.assertTrue(result == [("value1", "value2")])

    def test_num_retrieve(self):
        self.db.make_table(self.table_name, self.table_schema)
        self.db.insert_into_table(self.table_name, "key1", "value1")
        self.db.insert_into_table(self.table_name, "key1", "value2")
        self.db.insert_into_table(self.table_name, "key1", "value3")
        result = self.db.retrieve_from_table(self.table_name,
                                             self.table_schema.__iter__().__next__(),
                                             "key1",
                                             amount=1)
        self.assertTrue(result == [("key1", "value1")])

    def test_delete_table(self):
        self.db.make_table(self.table_name, self.table_schema)
        self.assertTrue(self.db.table_exists(self.table_name))
        self.db.delete_table(self.table_name)
        self.assertFalse(self.db.table_exists(self.table_name))

    def test_delete_from(self):
        self.db.make_table(self.table_name, self.table_schema)
        self.db.insert_into_table(self.table_name, "value1", "value2")
        self.db.insert_into_table(self.table_name, "value3", "value4")
        result = self.db.retrieve_from_table(self.table_name,
                                             self.table_schema.__iter__().__next__(),
                                             "value1")
        self.assertTrue(result == [("value1", "value2")])

        self.db.delete_from_table(self.table_name,
                                  self.table_schema.__iter__().__next__(),
                                  "value1")
        result = self.db.retrieve_from_table(self.table_name,
                                             self.table_schema.__iter__().__next__(),
                                             "value1")
        self.assertTrue(result == [])
        



