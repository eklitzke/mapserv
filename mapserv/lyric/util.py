from mapserv.lyric.table import AndExpr

def flatten_exprs(exprs):
    flattened = []
    for expr in exprs:
        if type(expr) is AndExpr:
            flattened.extend(flatten_exprs(expr.terms))
        else:
            flattened.append(expr)
    return flattened
