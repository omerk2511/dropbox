CONTROLLERS = {}

def controller(code):
    """
    Returns a wrapper function that registers a controller
    args: func
    ret: wrapper
    """

    def register_controller(func):
        CONTROLLERS[code] = func
        return func

    return register_controller

def get_controller_func(controller):
    """
    Returns a controller function that corresponds to a specific message code
    args: controller
    ret: controller_func
    """

    if controller in CONTROLLERS:
        return CONTROLLERS[controller]

    return None