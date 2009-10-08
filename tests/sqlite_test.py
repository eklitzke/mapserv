import unittest
import sqlite3

class SqliteTest(unittest.TestCase):

    def setUp(self):
        super(SqliteTest, self).setUp()
        self.conn = sqlite3.connect(':memory:')
