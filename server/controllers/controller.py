CONTROLLERS = {}

def controller(func):
    CONTROLLERS[func.__name__] = func
    return func

def get_controller_func(controller):
    if controller in CONTROLLERS:
        return CONTROLLERS[controller]

    raise Exception('Invalid controller.')