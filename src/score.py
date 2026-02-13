from src.outcomes import Outcomes


class Score:
    def __init__(self, score_entry):
        self.__id = score_entry.get('id')
        self.__points = score_entry.get('points')
        self.__duration = score_entry.get('duration')
        self.__level = score_entry.get('level')
        self.__outcome_id = score_entry.get('outcome_id')
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

    def __get_levels_possible_total(self, rule_sheet) -> int:
        max_points = 0
        for i in range(1, self.__level + 1):
            level_data = rule_sheet.get(f"level{i}")
            if level_data is not None:
                max_points += level_data.get('characterMax')
                if i < self.__level or self.__outcome_id == Outcomes.Win.value:
                    max_points += level_data.get('pass')
        return max_points

    def __get_duration_reward_if_applicable(self, rule_sheet) -> int:
        duration_reward = rule_sheet.get('durationReward')
        if (duration_reward is not None
                and self.__duration <= duration_reward.get('durationLimit')
                and self.__outcome_id == Outcomes.Win.value):
            return duration_reward.get('reward')
        else:
            return 0

    def check(self, rule_sheet):
        max_points = self.__get_levels_possible_total(rule_sheet) + self.__get_duration_reward_if_applicable(rule_sheet)
        return max_points >= self.__points
