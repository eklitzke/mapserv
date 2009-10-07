import unittest
from mapserv.lyric.table import Table
from mapserv.lyric.expression import *
from mapserv.interfaces.query.ttypes import *

class ExpressionTestCase(unittest.TestCase):

	def setUp(self):
		super(ExpressionTestCase, self).setUp()
		self.table = Table('test_table')
	
class SelectTestCase(ExpressionTestCase):

	def test_simple_select(self):
		expected = Query(clause=QueryClause(exprs=(Comparison(eqcomp=EqComparison(lhs=Target(col=Column(table='test_table', name='id', spatial=False)), rhs=Target(ival=100), eq=Equality.EQ)),)), variety=QueryType.SELECT)
		self.assertEqual(select(self.table.c.id == 100), expected)
	
	def test_select_with_null_comp(self):
		expected = Query(clause=QueryClause(exprs=(Comparison(nullcomp=NullComparison(isnull=True, col=Column(table='test_table', name='id', spatial=False))),)), variety=QueryType.SELECT)
		self.assertEqual(select(self.table.c.id == None), expected)

if __name__ == '__main__':
	unittest.main()
