from src.interaction import Interaction
from src.outcomes import Outcomes


class Score:
    def __init__(self, score_entry):
        self.__interactions = self.__parse_interactions_str(score_entry.get('interactions'))
        self.__duration = score_entry.get('duration')
        self.__level = score_entry.get('level')
        self.__outcome_id = score_entry.get('level')
        self.__player_id = score_entry.get('playerId')

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

    def __get_duration_reward_if_applicable(self, rule_sheet) -> int:
        duration_reward = rule_sheet.get('durationReward')
        if (duration_reward is not None
                and self.__duration <= duration_reward.get('durationLimit')
                and self.__outcome_id == Outcomes.Win.value):
            return duration_reward.get('reward')
        else:
            return 0

    def compute_score(self, rule_sheet) -> int:
        if self.__check_interactions(rule_sheet):
            return (
                    self.__get_duration_reward_if_applicable(rule_sheet)
                    + self.__get_level_pass_rewards(rule_sheet)
                    + self.__get_interaction_rewards(rule_sheet)
            )
        else:
             raise Exception('Interaction inconsistent with character counts in level games')

    @staticmethod
    def __parse_interactions_str(value: str):
        pairs = value.split('|')
        return map(
            lambda pair: Interaction(pair.split(',')),
            pairs
        )

    def __get_level_pass_rewards(self, rule_sheet) -> int:
        points = 0
        level_rewards = rule_sheet.get('levelRewards')
        for i in range(1, self.__level + 1):
            reward = level_rewards.get(i)
            if reward is not None:
                points += reward
        return points

    def __get_interaction_rewards(self, rule_sheet) -> int:
        points = 0
        interaction_rewards = rule_sheet.get('interactionRewards')
        for i in self.__interactions:
            reward = interaction_rewards.get(i.character_type)
            if reward is not None:
                points += reward * i.occurrences
        return points

    def __check_interactions(self, rule_sheet) -> bool:

        interaction_rewards = rule_sheet.get('interactionRewards')
        for i in self.__interactions:
            interaction_reward = interaction_rewards.get(i.character_type)
            if interaction_reward is not None and interaction_reward > 0:
                max_allowed_occurrences = 0
                for l in range(1, self.__level + 1):
                    level_max_interactions = rule_sheet.get('levelMaxInteractions').get(l)
                    if level_max_interactions is not None:
                        max_allowed_occurrences += level_max_interactions.get(i.character_type)
                if max_allowed_occurrences < i.occurrences:
                    return False
        return True
