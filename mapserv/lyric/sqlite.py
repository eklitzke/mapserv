import sqlite3
from mapserv.query.util import make_val
from mapserv.lyric.render import *

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
