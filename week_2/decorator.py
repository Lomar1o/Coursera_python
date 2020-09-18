from functools import wraps


def to_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return json.dumps(f(*args, **kwargs))
    return wrapper

