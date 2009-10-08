from mapserv.assertions import assert_not_reached
from mapserv.interfaces.query import ttypes

def make_target(t):
    if isinstance(t, ttypes.Target):
        return t
    elif hasattr(t, 'make_target'):
        return t.make_target()
    elif isinstance(t, ttypes.Column):
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

def make_orderby(order, ordering=None):
    if isinstance(order, ttypes.OrderClause):
        return order
    elif hasattr(order, 'make_orderby'):
        return order.make_orderby(ordering=ordering)

def make_val(t):
    if type(t) is not ttypes.Target:
        raise ValueError, 'Unexpected target: %r' % (t)

    if t.ival is not None:
        return t.ival
    elif t.fval is not None:
        return t.fval
    elif t.sval is not None:
        return t.val
    elif t.nullity is not None:
        return None
