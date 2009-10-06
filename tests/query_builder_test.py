import unittest

from mapserv.query import builder
from mapserv.query import util as query_util
from mapserv.interfaces.query import ttypes

class SelectBuilderTest(unittest.TestCase):

	def setUp(self):
		super(SelectBuilderTest, self).setUp()
		self.table_name = 'test'
		self.id_col = query_util.make_target(query_util.make_column('test.id'))

	def test_simple_select_one_eq(self):
		expected = 'SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id WHERE test_data.id = 10'
		rhs = query_util.make_target(10)
		eq_expr = query_util.make_comp(ttypes.EqComparison(eq=ttypes.Equality.EQ, lhs=self.id_col, rhs=rhs))
		q = ttypes.QueryClause(table=self.table_name, exprs=[eq_expr])
		self.assertEqual(builder.render_select(q), expected)
	
	def test_simple_select_multiple_eq(self):
		expected = 'SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id WHERE test_data.id <= -10 AND test_data.id != 0 AND test_data.id >= 10'

		exprs=[]

		add_expr = lambda e, r: exprs.append(query_util.make_comp(ttypes.EqComparison(eq=e, lhs=self.id_col, rhs=query_util.make_target(r))))
		add_expr(ttypes.Equality.LTE, -10)
		add_expr(ttypes.Equality.NEQ, 0)
		add_expr(ttypes.Equality.GTE, 10)
		q = ttypes.QueryClause(table=self.table_name, exprs=exprs)
		self.assertEqual(builder.render_select(q), expected)

if __name__ == '__main__':
	unittest.main()
