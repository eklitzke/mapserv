import unittest
from mapserv.lyric.table import Table
from mapserv.query.util import make_target
from mapserv.lyric.expression import *
from mapserv.lyric.render import *
from mapserv.interfaces.query.ttypes import *

class RenderSelectTestCase(unittest.TestCase):

	def setUp(self):
		super(RenderSelectTestCase, self).setUp()
		self.table = Table('render_test')

	def test_select(self):
		expected = ('SELECT render_test_data.*, render_test_tree.* '
					'FROM render_test_data INNER JOIN render_test_tree '
					'ON render_test_data.id = render_test_tree.id '
					'WHERE render_test_data.id IS NOT NULL')
		self.assertEqual(render_select(select(self.table.c.id != None)), expected)

if __name__ == '__main__':
	unittest.main()
