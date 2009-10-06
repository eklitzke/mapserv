from mapserv.assertions import assert_not_reached
from mapserv.interfaces.query import ttypes

def make_column(colname, spatial=False):
	table, name = colname.split('.')
	return ttypes.Column(table=table, name=name, spatial=spatial)

def make_target(t):
	if isinstance(t, ttypes.Column):
		return ttypes.Target(col=t)
	elif isinstance(t, (int, long)):
		return ttypes.Target(ival=t)
	elif isinstance(t, float):
		return ttypes.Target(fval=t)
	elif isinstance(t, basestring):
		return ttypes.Target(sval=t)
	elif t is None:
		return ttypes.Target(nullity=True)
	assert_not_reached('make_comp invalid arg: %r' % (t,))

def make_comp(comparator):
	if isinstance(comparator, ttypes.EqComparison):
		return ttypes.Comparison(eqcomp=comparator)
	elif isinstance(comparator, ttypes.NullComparison):
		return ttypes.Comparison(nullcomp=comparator)
	elif isinstance(comparator, ttypes.InComparison):
		return ttypes.comparator(incomp=comparator)
	assert_not_reached('make_comp invalid comparator: %r' % (comparator,))
