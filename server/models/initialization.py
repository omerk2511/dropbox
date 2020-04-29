INITIALIZERS = []

def initializer(func):
    INITIALIZERS.append(func)
    return func

def initialize_models():
    for initializer in INITIALIZERS:
        initializer()