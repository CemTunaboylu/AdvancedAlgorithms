from exceptions import Corrupt_Space
class Euclidean_N_Space:
        def __init__(self, corrupt_space_exception = Corrupt_Space):
                self.corrupt_space_exception =  corrupt_space_exception

        def __set_name(self, owner, name):
                self.private_name = "_" + name
                self.public_name = name
        def __set__(self, obj, value):
                if value < self.min_value:
                        raise self.below_exception

                if value > self.max_value:
                        raise self.above_exception

                setattr(obj, self.private_name, value)

        def __get__(self, obj, objtype=None):
                return getattr(obj, self.private_name)