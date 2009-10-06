import sqlite3
import contextlib

from mapserv.interfaces.mapserv import ttypes, GeoBoxService

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class ConnWrapper(object):
	def __init__(self, conn):
		self._conn = conn
	
	@contextlib.contextmanager
	def ro(self):
		yield self._conn.cursor()
		self._conn.rollback()
	
	@contextlib.contextmanager
	def rw(self):
		yield self._conn.cursor()
		self._conn.commit()
	
class GeoBoxHandler(object):

	def __init__(self):
		self.init_sqlite()

	def init_sqlite(self):
		self.conn = ConnWrapper(sqlite3.connect(':memory:'))

		with self.conn.rw() as c:
			c.execute('CREATE TABLE mapserv_data ('
					  'id INTEGER PRIMARY KEY, '
					  'timestamp REAL, '
					  'data BLOB)')
			c.execute('CREATE INDEX timestamp_idx ON mapserv_data (timestamp)') # XXX: try DESC
			c.execute('CREATE VIRTUAL TABLE mapserv_tree USING rtree ('
					  'id, '
					  'lat_nw, '
					  'lat_se, '
					  'lng_nw, '
					  'lng_se)')

	def insert(self, cell):
		data_query = 'INSERT INTO mapserv_data (timestamp, data) VALUES (?, ?)'
		tree_query = 'INSERT INTO mapserv_tree (id, lat_nw, lat_se, lng_nw, lng_se) VALUES (?, ?, ?, ?, ?)'

		with self.conn.rw() as c:
			c.execute(data_query, (cell.timestamp, cell.data))
			row_id = c.lastrowid
			c.execute(tree_query, (row_id, cell.pos.lat, cell.pos.lat, cell.pos.lng, cell.pos.lng))
		return row_id

	def expunge(self, row_id):
		data_query = 'DELETE FROM mapserv_data WHERE id = ?'
		tree_query = 'DELETE FROM mapserv_tree WHERE id = ?'

		with self.conn.rw() as c:
			c.execute(data_query, (row_id,))
			c.execute(tree_query, (row_id,))

	def select(self, q):
		query = ('SELECT mapserv_data.id, mapserv_tree.lat, mapserv_tree.lng, mapserv_data.timestamp, mapserv_data.data '
				 'FROM mapserv_data INNER JOIN mapserv_tree ON mapserv_data.id = mapserv_tree.id '
				 'WHERE mapserv_tree.lat >= ?'
				 ' AND mapserv_tree.lat <= ?'
				 ' AND mapserv_tree.lng >= ?'
				 ' AND mapserv_tree.lng <= ?')
		vals = [q.se.lat, q.nw.lat, q.nw.lng, q.se.lng]

		if q.start:
			query += ' AND mapserv_data.timestamp >= ?'
			vals.append(q.start)
		
		if q.sortby == ttypes.Sort.TIME_DESC:
			query += ' ORDER BY mapserv_data.timestamp DESC'
		elif q.sortby == ttypes.Sort.ID_DESC:
			query += ' ORDER BY mapserv_data.id DESC'
		elif q.sortby == ttypes.Sort.ID_ASC:
			query += ' ORDER BY mapsserv_data.id ASC'
		
		if q.limit:
			query += ' LIMIT ?'
			vals.append(q.limit)
		
		cells = []
		with self.conn.ro() as c:
			c.execute(query, vals)
			for id, lat, lng, timestamp, data in c.fetchall():
				pos = Coord(lat=lat, lng=lng)
				cells.append(Cell(id=id, pos=pos, timestamp=timestamp, data=data))
		return cells

def main(port=9009):
	handler = GeoBoxHandler()
	server = TServer.TSimpleServer(GeoBoxService.Processor(handler),
								   TSocket.TServerSocket(port),
								   TTransport.TBufferedTransportFactory(),
								   TBinaryProtocol.TBinaryProtocolFactory())
	server.serve()

if __name__ == '__main__':
	main()
