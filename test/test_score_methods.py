import unittest

from src.outcomes import Outcomes
from src.score import Score


class TestScoreMethods(unittest.TestCase):
    def setUp(self):
        self.__rulesheet = {
            'level1': {
                'characterMax': 2000,
                'pass': 100,
            },
            'level2': {
                'characterMax': 2500,
                'pass': 150,
            },
            'level3': {
                'characterMax': 2500,
                'pass': 150,
            },
            'durationReward': {
                'durationLimit': 200,
                'reward': 100,
            }
        }

    def test_valid_level1(self):
        score = Score({
            'id': 1,
            'points': 1900,
            'level': 1,
            'duration': 100,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), True)

    def test_invalid_level1(self):
        score = Score({
            'id': 1,
            'points': 2001,
            'level': 1,
            'duration': 100,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), False)

    def test_valid_level2(self):
        score = Score({
            'id': 1,
            'points': 4600,
            'level': 2,
            'duration': 100,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), True)

    def test_invalid_level2(self):
        score = Score({
            'id': 1,
            'points': 4601,
            'level': 2,
            'duration': 100,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), False)

    def test_valid_level3_within_duration_limit(self):
        score = Score({
            'id': 1,
            'points': 7500,
            'level': 3,
            'duration': 200,
            'outcome_id': Outcomes.Win.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), True)

    def test_invalid_level3_within_duration_limit(self):
        score = Score({
            'id': 1,
            'points': 7501,
            'level': 3,
            'duration': 200,
            'outcome_id': Outcomes.Win.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), False)

    def test_valid_level3_beyond_duration_limit(self):
        score = Score({
            'id': 1,
            'points': 7400,
            'level': 3,
            'duration': 201,
            'outcome_id': Outcomes.Win.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), True)

    def test_invalid_level3_beyond_duration_limit(self):
        score = Score({
            'id': 1,
            'points': 7401,
            'level': 3,
            'duration': 201,
            'outcome_id': Outcomes.Win.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), False)

    def test_valid_level3_loss(self):
        score = Score({
            'id': 1,
            'points': 7250,
            'level': 3,
            'duration': 201,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), True)

    def test_invalid_level3_loss(self):
        score = Score({
            'id': 1,
            'points': 7251,
            'level': 3,
            'duration': 201,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        })
        self.assertEqual(score.check(self.__rulesheet), False)

    if __name__ == '__main__':
        unittest.main()
