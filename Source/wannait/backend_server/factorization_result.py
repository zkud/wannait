import pickle
import os
from numpy import array


class FactorizationResult:
    def __init__(self, user_dict, recommendations):
        self._user_dict = user_dict
        self._recommendations = recommendations

    @property
    def user_dict(self) -> dict:
        return self._user_dict

    @user_dict.setter
    def user_dict_setter(self, new_value):
        self._user_dict = new_value

    @property
    def recommendations(self) -> array:
        return self._recommendations

    @recommendations.setter
    def recommendations_setter(self, new_value):
        self._recommendations = new_value

    def save(self):
        with open('result.ml', 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load():
        if os.path.exists('result.ml'):
            with open('result.ml', 'rb') as file:
                return pickle.load(file)
        else:
            return None

