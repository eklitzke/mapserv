import unittest
from tests import sqlite_test
from mapserv.lyric import *
from mapserv.interfaces.query.ttypes import *
from mapserv.query.util import make_target

class SqliteLyricTest(sqlite_test.SqliteTest):

    def setUp(self):
        super(SqliteLyricTest, self).setUp()
        self.table_name = 'test'
        self.cols = [Column(name='timestamp', spatial=False),
                     Column(name='lat', spatial=True),
                     Column(name='lng', spatial=True)]
        with rwtrans(self.conn) as cursor:
            cursor.execute('CREATE TABLE test_data (id INTEGER PRIMARY KEY, timestamp INTEGER)')
            cursor.execute('CREATE VIRTUAL TABLE test_tree USING rtree (id, lat_lo, lat_hi, lng_lo, lng_hi)')

    def test_insert(self):
        columns = dict(zip(self.cols, map(make_target, [100, 37.826458, -122.265182])))
        row = Row(table_name='test', columns=columns)
        row_id = insert(self.conn, row)
        with rotrans(self.conn, rollback=True) as cursor:
            cursor.execute('SELECT * FROM test_data WHERE id = ?', (row_id,))
            self.assertEqual(cursor.fetchone(), (row_id, 100))
            cursor.execute('SELECT COUNT(*) FROM test_tree WHERE id = ?', (row_id,))
            self.assertEqual(cursor.fetchone(), (1,))

    def test_existing_table_names(self):
        assert self.table_name in existing_table_names(self.conn)

if __name__ == '__main__':
    unittest.main()
