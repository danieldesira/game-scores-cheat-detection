import unittest

from src.inconsistent_level_interaction_exception import InconsistentLevelInteractionException
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
        self.__final_level = 3

    def test_level1(self):
        score = Score({
            'interactions': 'testPositive1,9|testNegative1,2',
            'level': 1,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        self.assertEqual(score.compute_score(self.__rulesheet), 35)
        self.assertEqual(score.outcome_id, Outcomes.Loss.value)

    def test_invalid_level1(self):
        score = Score({
            'interactions': 'testPositive1,11|testNegative1,2',
            'level': 1,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level2(self):
        score = Score({
            'interactions': 'testPositive1,20|testNegative1,5',
            'level': 2,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        self.assertEqual(score.compute_score(self.__rulesheet), 175)
        self.assertEqual(score.outcome_id, Outcomes.Loss.value)

    def test_invalid_level2(self):
        score = Score({
            'interactions': 'testPositive1,31|testNegative1,5',
            'level': 2,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level3(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 3,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        self.assertEqual(score.compute_score(self.__rulesheet), 375)
        self.assertEqual(score.outcome_id, Outcomes.Loss.value)

    def test_invalid_level3(self):
        score = Score({
            'interactions': 'testPositive1,51|testNegative1,5',
            'level': 3,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level4(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 4,
            'duration': 100,
            'player_id': 1,
        }, self.__final_level)
        self.assertEqual(score.compute_score(self.__rulesheet), 625)
        self.assertEqual(score.outcome_id, Outcomes.Win.value)

    if __name__ == '__main__':
        unittest.main()
