import unittest

from mapserv.query import builder
from mapserv.query import util as query_util
from mapserv.interfaces.query import ttypes

class SelectBuilderTest(unittest.TestCase):

	def setUp(self):
		super(SelectBuilderTest, self).setUp()
		self.table_name = 'test'
		self.id_col = query_util.make_target(query_util.make_column('test.id'))
	
	def mk_eq_expr(self, eq, rhs):
		return query_util.make_comp(ttypes.EqComparison(eq=eq, lhs=self.id_col, rhs=query_util.make_target(rhs)))

	def check_expected(self, q):
		self.assertEqual(builder.render_select(q), self.expected)

	def test_simple_select_one_eq(self):
		self.expected = ('SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id '
						 'WHERE test_data.id = 10')
		exprs = [self.mk_eq_expr(ttypes.Equality.EQ, 10)]
		self.check_expected(ttypes.QueryClause(table=self.table_name, exprs=exprs))
	
	def test_simple_select_multiple_eq(self):
		self.expected = ('SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id '
						 'WHERE test_data.id <= -10 AND test_data.id != 0 AND test_data.id >= 10')
		exprs = [self.mk_eq_expr(ttypes.Equality.LTE, -10),
				 self.mk_eq_expr(ttypes.Equality.NEQ, 0),
				 self.mk_eq_expr(ttypes.Equality.GTE, 10)]
		self.check_expected(ttypes.QueryClause(table=self.table_name, exprs=exprs))
	
	def test_simple_select_with_orderby(self):
		self.expected = ('SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id '
						 'WHERE test_data.id IS NOT NULL ORDER BY test_data.id ASC')
		exprs = [query_util.make_comp(ttypes.NullComparison(self.id_col, isnull=False))]
		orderby = [ttypes.OrderClause(col=query_util.make_column('test.id'))]
		self.check_expected(ttypes.QueryClause(table=self.table_name, exprs=exprs, orderby=orderby))

if __name__ == '__main__':
	unittest.main()
