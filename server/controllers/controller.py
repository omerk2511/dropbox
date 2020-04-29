CONTROLLERS = {}

def controller(code):
    def register_controller(func):
        CONTROLLERS[code] = func
        return func

    return register_controller

def get_controller_func(controller):
    if controller in CONTROLLERS:
        return CONTROLLERS[controller]

    return None