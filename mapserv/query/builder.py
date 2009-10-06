from mapserv.interfaces.query import ttypes
from mapserv.assertions import assert_not_reached

def render_order(order):
	if order == ttypes.Order.ASC:
		return 'ASC'
	elif order == ttypes.Order.DESC:
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
	return ('%s_tree.%s' if col.spatial else '%s_data.%s') % (col.table, col.name)

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
			return '%s IS NULL' % (render_target(c.col),)
		else:
			return '%s IS NOT NULL' % (render_target(c.col),)
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
	assert isinstance(q, ttypes.QueryClause)

	data_tbl = '%s_data' % (q.table)
	tree_tbl = '%s_tree' % (q.table)

	query = ['SELECT * FROM %(data_tbl)s',
			 'INNER JOIN %(tree_tbl)s ON %(data_tbl)s.id = %(tree_tbl)s.id',
			 'WHERE']
	query = [' '.join(query) % {'data_tbl': data_tbl, 'tree_tbl': tree_tbl}]
	query.append(' AND '.join(render_comparison(expr) for expr in q.exprs))

	if q.orderby:
		query.append(render_orderby(q.orderby))
	
	# N.B. For SQLite, offset only makes sense if a limit is specified
	if q.limit:
		query.append('LIMIT %d' % (q.limit,))
		if q.offset:
			query.append('OFFSET %d' % (q.offset,))
	
	return ' '.join(query)
