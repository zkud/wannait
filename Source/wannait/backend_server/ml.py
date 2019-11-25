import torch

class FactorizationModel:
    """ Singleton object, responsible for updating
    and storing matrix factorization ml algorithm results """
    _result = None

    def __init__(self):
        pass

    def regenerate(self):
        pass

    def recommendation_indexes(self, user_id: int):
        return [0]

    def user_is_here(self, user_id: int):
        return False

    @staticmethod
    def get_instance():
        if FactorizationModel._result is None:
            FactorizationModel._result = FactorizationModel()

        return FactorizationModel._result
