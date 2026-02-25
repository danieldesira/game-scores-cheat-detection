from lib.inconsistent_level_interaction_exception import InconsistentLevelInteractionException
from lib.interaction import Interaction
from lib.outcomes import Outcomes


class Score:
    def __init__(self, score_entry, final_level: int):
        self.__interactions = self.__parse_interactions_str(score_entry.get('interactions'))
        self.__duration = score_entry.get('duration')
        self.__level = score_entry.get('level')
        if score_entry.get('level') > final_level:
            self.__outcome = Outcomes.Win.value
        else:
            self.__outcome = Outcomes.Loss.value
        self.__player_id = score_entry.get('playerId')
        self.__timestamp = score_entry.get('timestamp')

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def level(self) -> int:
        return self.__level

    @property
    def outcome(self) -> str:
        return self.__outcome

    @property
    def player_id(self) -> int:
        return self.__player_id

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    def __get_duration_reward_if_applicable(self, rule_sheet) -> int:
        duration_reward = rule_sheet.get('durationReward')
        if (duration_reward is not None
                and self.__duration <= duration_reward.get('durationLimit')
                and self.__outcome == Outcomes.Win.value):
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
            raise InconsistentLevelInteractionException()

    @staticmethod
    def __parse_interactions_str(value: str):
        if value is not None:
            pairs = value.split('|')
            return list(map(
                lambda pair: Interaction(pair.split(',')),
                pairs
            ))
        else:
            return None

    def __get_level_pass_rewards(self, rule_sheet) -> int:
        points = 0
        level_rewards = rule_sheet.get('levelRewards')
        for i in range(1, self.__level):
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
        for interaction in self.__interactions:
            interaction_reward = interaction_rewards.get(interaction.character_type)
            if interaction_reward is not None and interaction_reward > 0:
                max_allowed_occurrences = 0
                for level in range(1, self.__level + 1):
                    level_max_interactions = rule_sheet.get('levelMaxInteractions').get(str(level))
                    if level_max_interactions is not None:
                        character_level_max_occurrences = level_max_interactions.get(interaction.character_type)
                        if character_level_max_occurrences is not None:
                            max_allowed_occurrences += character_level_max_occurrences
                if max_allowed_occurrences < interaction.occurrences:
                    return False
        return True
