class Interaction:
    def __init__(self, l: list):
        self.__character_type = l[0]
        self.__occurrences = int(l[1])

    @property
    def character_type(self):
        return self.__character_type

    @property
    def occurrences(self):
        return self.__occurrences
