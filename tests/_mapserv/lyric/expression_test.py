import unittest
from mapserv.lyric.table import Table
from mapserv.query.util import make_target
from mapserv.lyric.expression import *
from mapserv.interfaces.query.ttypes import *

class ExpressionTestCase(unittest.TestCase):

    def setUp(self):
        super(ExpressionTestCase, self).setUp()
        self.table = Table('test_table')

        self.id_col = Column(table='test_table', name='id', spatial=False)
        self.id_eq_100 = Comparison(eqcomp=EqComparison(lhs=Target(col=self.id_col), rhs=Target(ival=100), eq=Equality.EQ))
        self.id_lt_100 = Comparison(eqcomp=EqComparison(lhs=Target(col=self.id_col), rhs=Target(ival=100), eq=Equality.LT))
        self.id_is_null = Comparison(nullcomp=NullComparison(isnull=True, col=self.id_col))
        self.id_not_null = Comparison(nullcomp=NullComparison(isnull=False, col=self.id_col))

    def _make_query(self, **kwargs):
        kw = {'clause': QueryClause(**kwargs), 'variety': self.VARIETY}
        return Query(**kw)

class SelectTestCase(ExpressionTestCase):

    VARIETY = QueryType.SELECT

    def test_simple_select(self):
        expected = self._make_query(exprs=(self.id_eq_100,))
        self.assertEqual(select(self.table.c.id == 100), expected)

    def test_select_with_null_comp(self):
        expected = self._make_query(exprs=(self.id_is_null,))
        self.assertEqual(select(self.table.c.id == None), expected)

    def test_select_with_not_null_comp(self):
        expected = self._make_query(exprs=(self.id_not_null,))
        self.assertEqual(select(self.table.c.id != None), expected)

    def test_select_multiple_exprs(self):
        expected = self._make_query(exprs=(self.id_lt_100, self.id_not_null))
        self.assertEqual(select(self.table.c.id < 100, self.table.c.id != None), expected)

    def test_select_with_single_orderby(self):
        expected = self._make_query(exprs=(self.id_lt_100,), orderby=[OrderClause(col=self.id_col)])
        self.assertEqual(select(self.table.c.id < 100, orderby=self.table.c.id), expected)

    def test_select_with_multi_orderby(self):
        expected = self._make_query(exprs=(self.id_lt_100,), orderby=[OrderClause(col=self.id_col), OrderClause(col=self.id_col, order=Order.DESC)])
        self.assertEqual(select(self.table.c.id < 100, orderby=[self.table.c.id, self.table.c.id.desc()]), expected)

    def test_select_with_limit(self):
        expected = self._make_query(exprs=(self.id_not_null,), limit=5)
        self.assertEqual(select(self.table.c.id != None, limit=5), expected)

    def test_select_with_limit_and_offset(self):
        expected = self._make_query(exprs=(self.id_not_null,), limit=5, offset=10)
        self.assertEqual(select(self.table.c.id != None, limit=5, offset=10), expected)

class DeleteTestCase(ExpressionTestCase):

    VARIETY = QueryType.DELETE

    def test_simple_delete(self):
        expected = self._make_query(exprs=(self.id_eq_100,))
        self.assertEqual(delete(self.table.c.id == 100), expected)

    def test_delete_with_limit(self):
        expected = self._make_query(exprs=(self.id_eq_100,), limit=100)
        self.assertEqual(delete(self.table.c.id == 100, limit=100), expected)

class InsertTestCase(ExpressionTestCase):

    def setUp(self):
        super(InsertTestCase, self).setUp()
        self.lat = 37.813369
        self.lng = -122.276866

    def _make_insert(self, **kwargs):
        kw = dict((k, make_target(v)) for k, v in kwargs.iteritems())
        row = Row(table_name='test_table', columns=kw)
        return Query(variety=QueryType.INSERT, insert_row=row)

    def test_insert(self):
        expected = self._make_insert(lat=self.lat, lng=self.lng)
        self.assertEqual(insert(self.table, lat=self.lat, lng=self.lng), expected)

    def test_insert_no_cols(self):
        self.assertRaises(ValueError, insert, self.table)

    def test_insert_with_id_column(self):
        self.assertRaises(ValueError, lambda: insert(self.table, id=100, lat=self.lat, lng=self.lng))

if __name__ == '__main__':
    unittest.main()
