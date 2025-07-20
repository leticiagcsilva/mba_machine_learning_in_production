class WeightSensor:
    def __init__(self):
        self.__weight = 0.0

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value
