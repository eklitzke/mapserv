import mapserv.query.util
from mapserv.interfaces.query import ttypes
from mapserv.decorators import restrict_kw

def make_clause(exprs, orderby=None, limit=None, offset=None):
	"""Make the WHERE/ORDER BY/LIMIT part of a SELECT, UPDATE, or DELETE query.
	"""
	assert exprs, 'Must supply exprs to make_clause! (got: %r)' % (exprs,)
	assert all(isinstance(expr, ttypes.Comparison) for expr in exprs)

	kwargs = {'exprs': exprs}
	if orderby is not None:
		if isinstance(orderby, (list, tuple)):
			kwargs['orderby'] = list(orderby)
		else:
			kwargs['orderby'] = [orderby]
	if limit is not None:
		kwargs['limit'] = limit
		if offset:
			kwargs['offset'] = offset
	
	return ttypes.QueryClause(**kwargs)

@restrict_kw('orderby', 'limit', 'offset')
def select(*args, **kwargs):
	clause = make_clause(args, orderby=kwargs.get('orderby'), limit=kwargs.get('limit'), offset=kwargs.get('offset'))
	return ttypes.Query(variety=ttypes.QueryType.SELECT, clause=clause)

@restrict_kw('limit')
def update(*args, **kwargs):
	clause = make_clause(args, limit=kwargs.get('limit'))
	return ttypes.Query(variety=ttypes.QueryType.UPDATE, clause=clause)

@restrict_kw('limit')
def delete(*args, **kwargs):
	clause = make_clause(args, limit=kwargs.get('limit'))
	return ttypes.Query(variety=ttypes.QueryType.DELETE, clause=clause)

def insert(table, **kwargs):
	columns = dict((k, mapserv.query.util.make_target(v)) for k, v in kwargs.iteritems())
	row = ttypes.Row(table_name=table.name, columns=columns)
	return ttypes.Query(variety=ttypes.QueryType.INSERT, insert_row=row)
