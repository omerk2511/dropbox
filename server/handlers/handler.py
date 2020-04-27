HANDLERS = {}

def handler(func):
    HANDLERS[func.__name__] = func
    return func

def get_handler_func(handler):
    if handler in HANDLERS:
        return HANDLERS[handler]

    raise Exception('Invalid handler.')