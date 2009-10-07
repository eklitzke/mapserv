from mapserv.interfaces.query import ttypes
import mapserv.query.util

class PseudoColumn(object):

	def __init__(self, table, name, spatial):
		self.table = table
		self.name = name
		self.spatial = spatial
	
	def make_target(self):
		col = ttypes.Column(table=self.table, name=self.name, spatial=self.spatial)
		return ttypes.Target(col=col)

	def compare_to(self, other, eq):
		lhs = self.make_target()
		rhs = mapserv.query.util.make_target(other)
		eqcomp = ttypes.EqComparison(eq=eq, rhs=rhs, lhs=lhs)
		return ttypes.Comparison(eqcomp=eqcomp)

	def __lt__(self, other):
		return self.compare_to(other, ttypes.Equality.LT)

	def __le__(self, other):
		return self.compare_to(other, ttypes.Equality.LTE)

	def __eq__(self, other):
		if other is None:
			col = ttypes.Column(table=self.table, name=self.name, spatial=self.spatial)
			nullcomp = ttypes.NullComparison(col=col, isnull=True)
			return ttypes.Comparison(nullcomp=nullcomp)
		else:
			return self.compare_to(other, ttypes.Equality.EQ)
	
	def __ne__(self, other):
		if other is None:
			col = ttypes.Column(table=self.table, name=self.name, spatial=self.spatial)
			nullcomp = ttypes.NullComparison(col=col, isnull=False)
			return ttypes.Comparison(nullcomp=nullcomp)
		else:
			return self.compare_to(other, ttypes.Equality.NEQ)
	
	def __gt__(self, other):
		return self.compare_to(other, ttypes.Equality.GT)

	def __ge__(self, other):
		return self.compare_to(other, ttypes.Equality.GTE)

	def make_in_comparison(self, others, notin):
		targets = [mapserv.query.util.make_target(x) for x in others]
		incomp = ttypes.InComparison(lhs=self.make_target(), targets=targets, notin=notin)
		return ttypes.Comparison(incomp=incomp)

	def in_(self, others):
		return self.make_in_comparison(others, False)

	def notin(self, others):
		return self.make_in_comparison(others, True)
	notin_ = notin

class ColumnMaker(object):

	def __init__(self, table, spatial):
		self.table = table
		self.spatial = spatial
	
	def __getattr__(self, name):
		return PseudoColumn(self.table, name, self.spatial)

class Table(object):

	def __init__(self, name):

		self.name = name

		# Makes norma, "data" columns
		self.c = ColumnMaker(self.name, False)

		# Makes spatial columns
		self.s = ColumnMaker(self.name, True)
