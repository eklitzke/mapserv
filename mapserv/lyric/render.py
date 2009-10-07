from mapserv.interfaces.query import ttypes
from mapserv.assertions import assert_not_reached
from mapserv.thrift.introspection import walk_thrift

def render_table(table_name, spatial):
    return table_name + ('_tree' if spatial else '_data')

def render_order(order):
    if order == types.Order.ASC:
        return 'ASC'
    elif order == types.Order.DESC:
        return 'DESC'
    assert_not_reached('invalid order: %r' % (order,))

def render_eq(kind):
    EQ_REPRESENTATION = {
        ttypes.Equality.EQ: '=',
        ttypes.Equality.NEQ: '!=',
        ttypes.Equality.LT: '<',
        ttypes.Equality.LTE: '<=',
        ttypes.Equality.GT: '>',
        ttypes.Equality.GTE: '>='
    }
    return EQ_REPRESENTATION[kind]

def render_column(col):
    return '%s.%s' % (render_table(col.table, col.spatial), col.name)

def render_target(targ):
    if targ.col:
        return render_column(targ.col)
    elif targ.ival:
        return '%d' % (targ.ival,)
    elif targ.fval:
        return '%s' % (targ.fval,)
    elif targ.sval:
        return '%s' % (targ.sval,)
    elif targ.nullity is not None:
        return 'NULL'
    assert_not_reached('invalid target: %r' % (targ,))

def render_comparison(comp):
    if comp.eqcomp:
        c = comp.eqcomp
        return '%s %s %s' % (render_target(c.lhs), render_eq(c.eq), render_target(c.rhs))
    elif comp.nullcomp:
        c = comp.nullcomp
        if c.isnull:
            return '%s IS NULL' % (render_column(c.col),)
        else:
            return '%s IS NOT NULL' % (render_column(c.col),)
    elif comp.incomp:
        c = comp.incomp
        if len(c.targets) == 0:
            return '1' if c.notin else '0'
        else:
            in_text = 'NOT IN' if c.notin else 'IN'
            return '%s %s (%s)' % (render_target(c.lhs), in_text, ', '.join(render_target(targ) for targ in c.targets))
    assert_not_reached('invalid render_comparison: %r' % (comp,))

def render_orderby(order):
    clauses = ', '.join('%s %s' % (render_column(c.col), render_order(c.order)) for c in order)
    return 'ORDER BY ' + clauses

def render_select(q):
    if isinstance(q, ttypes.Query):
        assert q.variety == ttypes.QueryType.SELECT
        q = q.clause
    assert isinstance(q, ttypes.QueryClause)

    cols = []
    for expr in q.exprs:
        cols.extend(obj for obj in walk_thrift(expr) if isinstance(obj, ttypes.Column))
    assert cols, 'No expresions included columns!'
    tbls = set(col.table for col in cols if col.table)
    assert len(tbls) == 1, 'Expected 1 table, instead saw %d' % (len(tbls),)
    table_name = tbls.pop()

    data_table = render_table(table_name, False)
    tree_table = render_table(table_name, True)
    query = ['SELECT %(data_table)s.*, %(tree_table)s.* FROM %(data_table)s',
             'INNER JOIN %(tree_table)s ON %(data_table)s.id = %(tree_table)s.id',
             'WHERE']
    query = [' '.join(query) % {'data_table': data_table, 'tree_table': tree_table}]
    query.append(' AND '.join(render_comparison(expr) for expr in q.exprs))

    if q.orderby:
        query.append(render_orderby(q.orderby))

    # N.B. For SQLite, offset only makes sense if a limit is specified
    if q.limit:
        query.append('LIMIT %d' % (q.limit,))
        if q.offset:
            query.append('OFFSET %d' % (q.offset,))

    return ' '.join(query)

__all__ = ['render_select']
