from background_task import background
import torch # need for reatrain safely runnging
import numpy as np
import math


from backend_server.factorization_result import FactorizationResult


class FactorizationModel:
    """ Singleton object, responsible for updating
    and storing matrix factorization ml algorithm results """
    _result = None

    def __init__(self):
        self.result: FactorizationResult = FactorizationResult.load()

    def retrain(self):
        exec(open('./backend_server/retrain.py').read())
        self.result: FactorizationResult = FactorizationResult.load()

    def recommendation_indexes(self, user_id: int):
        if self.result is not None:
            if user_id in self.result.user_dict.keys():
                row = self.result.user_dict[user_id]
                return self.result.recommendations[row, :]

        return []

    def user_is_here(self, user_id: int):
        if self.result is not None:
            if user_id in self.result.user_dict.keys():
                return True

        return False

    @staticmethod
    def get_instance():
        if FactorizationModel._result is None:
            FactorizationModel._result = FactorizationModel()

        return FactorizationModel._result


@background(schedule=15 * 60)
def retrain():
    FactorizationModel.get_instance().retrain()

