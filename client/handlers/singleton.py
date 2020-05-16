class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Returns an instance if exists, otherwise returns a new instance
        args: cls, *args, **kwargs
        ret: instance
        """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]