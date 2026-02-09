class Score:
    def __init__(self, score_entry):
        self.__id = score_entry.get('id')
        self.__points = score_entry.get('points')
        self.__duration = score_entry.get('duration')
        self.__level = score_entry.get('level')
        self.__outcome_id = score_entry.get('outcome_id')
        self.__duration = score_entry.get('duration')
        self.__player_id = score_entry.get('player_id')

    @property
    def id(self):
        return self.__id

    def check(self, sheet):
        max_points = 0
        level = self.__level
        for i in range(1, level + 1):
            level_data = sheet.get(f"level{i}")
            if level_data is not None:
                max_points += level_data.get('characterMax')
        return max_points >= self.__points
