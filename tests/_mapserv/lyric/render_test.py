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
        self.cols_no_id = ['lng', 'lat']
        self.cols_with_id = ['id'] + self.cols_no_id

    def test_render_select(self):
        expected = ('SELECT render_test_data.*, render_test_tree.* '
                    'FROM render_test_data INNER JOIN render_test_tree '
                    'ON render_test_data.id = render_test_tree.id '
                    'WHERE render_test_data.id IS NOT NULL')
        self.assertEqual(render_select(select(self.table.c.id != None)), expected)

    def test_render_insert_nonspatial(self):
        expected = 'INSERT INTO render_test_data (lng, lat) VALUES (?, ?)'
        self.assertEqual(render_insert(self.table.name, self.cols_no_id, False), expected)

    def test_render_insert_spatial(self):
        expected = 'INSERT INTO render_test_tree (id, lng, lat) VALUES (?, ?, ?)'
        self.assertEqual(render_insert(self.table.name, self.cols_with_id, True), expected)

    def test_render_insert_nonspatial_with_id(self):
        self.assertRaises(ValueError, render_insert, self.table.name, self.cols_with_id, False)

    def test_render_insert_spatial_without_id(self):
        self.assertRaises(ValueError, render_insert, self.table.name, self.cols_no_id, True)

if __name__ == '__main__':
    unittest.main()
