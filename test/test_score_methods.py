import unittest

from src.outcomes import Outcomes
from src.score import Score


class TestScoreMethods(unittest.TestCase):
    def setUp(self):
        self.__rulesheet = {
            'levelRewards': {
                1: 100,
                2: 150,
                3: 150,
            },
            'interactionRewards': {
                'testPositive1': 5,
                'testNegative1': -5,
                'testPositive2': 10,
                'testNegative2': -10,
                'testPositive3': 15,
                'testNegative3': -15,
            },
            'levelMaxInteractions': {
                1: {
                    'testPositive1': 10,
                    'testPositive2': 10,
                },
                2: {
                    'testPositive1': 20,
                    'testPositive2': 10,
                },
                3: {
                    'testPositive1': 20,
                    'testPositive2': 20,
                    'testPositive3': 5,
                },
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
