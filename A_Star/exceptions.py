class A_Star_Exception(Exception): pass

class Corrupt_Space(A_Star_Exception): 
        def __init__(self, msg:str="The space is corrupt, there are missing coordinates for dimensions."):
                self.message = msg
                super().__init__(self.message)

        def __str__(self):
                