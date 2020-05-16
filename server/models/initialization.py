INITIALIZERS = []

def initializer(func):
    """
    Registers an initializer function
    args: func
    ret: func
    """

    INITIALIZERS.append(func)
    return func

def initialize_models():
    """
    Initializes all the tables
    args: none
    ret: none
    """

    for initializer in INITIALIZERS:
        initializer()