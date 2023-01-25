from functools import wraps


def permission(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.api, str) or not isinstance(self.secret, str):
            raise PermissionError('Set API or Secret key')
        return fn(self, *args, **kwargs)
    return wrapper
