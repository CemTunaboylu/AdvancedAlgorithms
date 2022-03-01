import types
class StaticTypeImposed:
    def __init__(self, 
                 imposed_type, 
                 value,
                 already_set_exception=ValueError,
                 type_error=TypeError):
        self.already_set_exception = already_set_exception
        self.type_error = type_error
        self.imposed_type = imposed_type
        self.value =  value

    def __set__(self, obj, value):
        if isinstance(value, self.imposed_type):
            self.value =  value
        # elif self.value != None: raise self.already_set_exception(f"Object is already set.")
        else: raise self.type_error(f"{value} is imposed to be of {self.imposed_type}")

    def __get__(self, obj, objtype=None):
        if obj is None:
            print(f"OBJ is NONE")
            return self
        # return getattr(obj, self.name)
        return self.value


class IsBetween:
    def __init__(self,
                 min_value, 
                 max_value, 
                 below_exception=ValueError(),                        
                 above_exception=ValueError()):
        self.min_value = min_value
        self.max_value = max_value

        self.below_exception = below_exception
        self.above_exception = above_exception

    def __set_name__(self, owner, name):
        self.name = '_' + name
        self.public_name = name

    def __set__(self, obj, value):
        if value < self.min_value:
            raise self.below_exception

        if value > self.max_value:
            raise self.above_exception

        setattr(obj, self.private_name, value)

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

class Car:

    fuel_amount = IsBetween(0, 60, ValueError(), ValueError())

    def __init__(self):
        self.fuel_amount = 0

def test():
    c = Car()
    c.fuel_amount = 50 
    print(c.fuel_amount)
    try:
        c.fuel_amount = 70
        print(c.fuel_amount)
    except Exception as e:
        assert isinstance(e, ValueError)
    try:
        c.fuel_amount = -10
        print(c.fuel_amount)
    except Exception as e:
        assert isinstance(e, ValueError)

if __name__ == "__main__":
    test()