import sqlite3
from mapserv.query.util import make_val
from mapserv.lyric.render import *
from mapserv.interfaces.query import ttypes
from mapserv.lyric.table import Table

class SqliteContext(object):

    def __init__(self, conn, rollback=False, cursor_cls=None):
        self.conn = conn
        self.rollback_first = rollback
        self.cursor_cls = cursor_cls

    def __enter__(self):
        if self.rollback_first:
            self.conn.rollback()
        if self.cursor_cls:
            return self.conn.cursor(self.cursor_cls)
        return self.conn.cursor()

    def __exit__(self):
        raise NotImplementedError

class rwtrans(SqliteContext):
    """This context manager yields a cursor when entered. When exited, it rolls
    back upon an exception, and commits otherwise.
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()

class rotrans(SqliteContext):
    """This context manager unconditionally rolls back after exiting its
    context.
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.rollback()

def insert(conn, row):
    """Insert a row into SQLite"""
    data_names, data_vals = [], []
    spatial_names, spatial_vals = [], []
    for col, target in row.columns.iteritems():
        val = make_val(target)
        if col.spatial:
            spatial_vals.extend([val, val])
            spatial_names.extend(['%s_lo' % col.name, '%s_hi' % col.name])
        else:
            data_vals.append(val)
            data_names.append(col.name)

    data_insert = render_insert(row.table_name, data_names, False)
    spatial_insert = render_insert(row.table_name, ['id'] + spatial_names, True)

    with rwtrans(conn) as cursor:
        cursor.execute(data_insert, data_vals)
        row_id = cursor.lastrowid
        cursor.execute(spatial_insert, [row_id] + spatial_vals)
    return row_id

def create(conn, name, columns):

    data_columns = ['id INTEGER PRIMARY KEY']
    spatial_columns = ['id']

    for col in columns:
        for coltype in ['INTEGER', 'REAL', 'TEXT', 'BLOB']:
            if col.type == getattr(ttypes.ColumnType, coltype):
                data_columns.append('%s %s' % (col.name, coltype))
                break
        else:
            assert col.type == ttypes.ColumnType.SPATIAL
            spatial_columns.append(col.name)

    with rwtrans(conn) as cursor:
        cursor.execute('CREATE TABLE %s_data (%s)' % (name, ', '.join(data_columns)))
        cursor.execute('CREATE TABLE %s_tree (%s)' % (name, ', '.join(spatial_columns)))
    
    return Table.ref(name)

def drop(conn, name, if_exists=True):

    def _drop(cursor, table_name):
        if if_exists:
            cursor.execute('DROP TABLE IF EXISTS %s' % table_name)
        else:
            cursor.execute('DROP TABLE %s' % table_name)

    with rwtrans(conn) as cursor:
        _drop(cursor, name + '_data')
        _drop(cursor, name + '_tree')

def existing_table_names(conn):
    with rotrans(conn) as cursor:
        cursor.execute('SELECT name FROM sqlite_master '
                       'WHERE type = ?'
                       ' AND (name LIKE ? OR name LIKE ?) ',
                       ('table', '%_data', '%_tree'))
        rows = cursor.fetchall()
    table_names = set()
    for row in rows:
        table_name, = row
        table_names.add(str(table_name.rsplit('_', 1)[0]))
    return list(table_names)
