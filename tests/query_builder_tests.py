import unittest

from mapserv.query import builder
from mapserv.query import util as query_util
from mapserv.interfaces.query import ttypes

class SelectBuilderTest(unittest.TestCase):

	def test_simple_select_one_eq(self):

		expected = 'SELECT * FROM test_data INNER JOIN test_tree ON test_data.id = test_tree.id WHERE test_data.id = 10'

		col = query_util.make_target(query_util.make_column("test.id"))
		rhs = query_util.make_target(10)
		eq_expr = query_util.make_comp(ttypes.EqComparison(eq=ttypes.Equality.EQ, lhs=col, rhs=rhs))
		q = ttypes.QueryClause(table='test', exprs=[eq_expr])
		self.assertEqual(builder.render_select(q), expected)

if __name__ == '__main__':
	unittest.main()
