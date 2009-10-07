import functools

def restrict_kw(*allowed):
    """Restrict the kwargs a function can take. Example usage:

    @restrict_kw('foo, 'bar')
    def myfunc(*args, **kwargs):
        ...

    If any kwargs other than 'foo' or 'bar' are sent to myfunc, then an
    AssertionError will be raised.
    """
    allowed_set = set(allowed)
    def inner_decorator(func):
        @functools.wraps(func)
        def closure(*args, **kwargs):
            extra_kw = set(kwargs.keys()) - allowed_set
            if extra_kw:
                raise AssertionError("Got extra kwargs %s, only %s allowed" % (list(extra_kw), list(allowed)))
            return func(*args, **kwargs)
        return closure
    return inner_decorator
