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
            'interactions': 'testPositive1,9|testNegative1,2',
            'level': 1,
            'duration': 100,
            'outcome_id': Outcomes.Loss.value,
            'player_id': 1,
        }, 1)
        self.assertEqual(score.compute_score(self.__rulesheet), 135)

    if __name__ == '__main__':
        unittest.main()
