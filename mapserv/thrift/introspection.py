def is_thrift_obj(obj):
    return hasattr(obj, 'thrift_spec')

def walk_thrift(obj):
    """Returns a generator that does a BFS on the thrift structure, yielding
    items it finds. Cyclic structures are OK.
    """
    if not is_thrift_obj(obj):
        raise TypeError, 'Object %r was not a thrift structure' % (obj,)

    seen_ids = set()

    def walk_obj(o):
        q = []
        for attr in o.thrift_spec:
            if attr is None:
                continue
            thing = getattr(o, attr[2])
            if is_thrift_obj(thing) and id(thing) not in seen_ids:
                q.append(thing)
                seen_ids.add(id(thing))
                yield thing
        for thing in q:
            for item in walk_obj(thing):
                yield item

    return walk_obj(obj)
