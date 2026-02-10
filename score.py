from outcomes import Outcomes


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
    def id(self) -> int:
        return self.__id

    @property
    def points(self) -> int:
        return self.__points

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def level(self) -> int:
        return self.__level

    @property
    def outcome_id(self) -> int:
        return self.__outcome_id

    @property
    def player_id(self) -> int:
        return self.__player_id

    def check(self, sheet):
        max_points = 0
        level = self.__level
        for i in range(1, level + 1):
            level_data = sheet.get(f"level{i}")
            if level_data is not None:
                max_points += level_data.get('characterMax')
                if i < level or self.__outcome_id == Outcomes.Win:
                    max_points += level_data.get('pass')
        return max_points >= self.__points
