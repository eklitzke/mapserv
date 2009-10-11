import threading
import weakref

from mapserv.interfaces.query import ttypes
import mapserv.query.util

class AndExpr(object):
    """Logically group a series of expressions by AND."""
    def __init__(self, *terms):
        self.terms = terms

class PseudoColumn(object):

    def __init__(self, table, name, spatial):
        self.table = table
        self.name = name
        self.spatial = spatial
    
    def make_target(self):
        col = ttypes.Column(table=self.table, name=self.name, spatial=self.spatial)
        return ttypes.Target(col=col)

    def make_orderby(self, ordering=None):
        col = ttypes.Column(table=self.table, name=self.name, spatial=self.spatial)
        return ttypes.OrderClause(col=col, order=ordering)

    def asc(self):
        return self.make_orderby(ttypes.Order.ASC)

    def desc(self):
        return self.make_orderby(ttypes.Order.DESC)

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

class PseudoDataColumn(PseudoColumn):

    def __init__(self, table, name):
        super(PseudoDataColumn, self).__init__(table, name, spatial=False)

class PseudoSpatialColumn(PseudoColumn):

    def __init__(self, table, name):
        self.table = table
        self.name = name

    def make_cols(self):
        lo = PseudoColumn(self.table, self.name + '_lo', spatial=True)
        hi = PseudoColumn(self.table, self.name + '_hi', spatial=True)
        return lo, hi

    def __eq__(self, other):
        lo, hi = self.make_cols()
        return AndExpr(lo == other, hi == other)

    def __ne__(self, other):
        lo, hi = self.make_cols()
        return AndExpr(lo != other, hi != other)

    def __le__(self, other):
        raise NotImplementedError('__le__ Invalid for spatial columns')

    def __lt__(self, other):
        raise NotImplementedError('__lt__ Invalid for spatial columns')

    def __gt__(self, other):
        raise NotImplementedError('__gt__ Invalid for spatial columns')

    def __ge__(self, other):
        raise NotImplementedError('__ge__ Invalid for spatial columns')

    def between(self, lo_val, hi_val, inclusive=True):
        assert lo_val <= hi_val
        lo, hi = self.make_cols()
        if inclusive:
            return AndExpr(lo >= lo_val, hi <= hi_val)
        else:
            return AndExpr(lo > lo_val, hi < hi_val)

class ColumnMaker(object):

    PSEUDO_CLS = None

    def __init__(self, table):
        self.table = table
    
    def __getattr__(self, name):
        return self.PSEUDO_CLS(self.table, name)

class DataColumnMaker(ColumnMaker):
    PSEUDO_CLS = PseudoDataColumn

class SpatialColumnMaker(ColumnMaker):
    PSEUDO_CLS = PseudoSpatialColumn
    
class Table(object):

    #_table_cache = weakref.WeakValueDictionary()
    _table_cache = {}
    _table_cache_lock = threading.Lock()

    def __init__(self, name):
        assert self.__class__._table_cache_lock.locked(), "Create new references using Table.ref()"

        self.name = name

        # Makes normal, "data" columns
        self.c = DataColumnMaker(self.name)

        # Makes spatial columns
        self.s = SpatialColumnMaker(self.name)

    @classmethod
    def ref(cls, table_name):
        with cls._table_cache_lock:
            cls._table_cache.setdefault(table_name, cls(table_name))
            return cls._table_cache[table_name]

__all__ = ['Table']
