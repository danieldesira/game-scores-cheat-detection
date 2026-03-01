import unittest

from lib.inconsistent_level_interaction_exception import InconsistentLevelInteractionException
from lib.invalid_resets_exception import InvalidResetsException
from lib.outcomes import Outcomes
from lib.score import Score


class TestScoreMethods(unittest.TestCase):
    def setUp(self):
        self.__rulesheet = {
            'levelRewards': {
                '1': 100,
                '2': 150,
                '3': 150,
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
                '1': {
                    'testPositive1': 10,
                    'testPositive2': 10,
                },
                '2': {
                    'testPositive1': 20,
                    'testPositive2': 10,
                },
                '3': {
                    'testPositive1': 20,
                    'testPositive2': 20,
                    'testPositive3': 5,
                },
            },
            'durationReward': {
                'durationLimit': 200,
                'reward': 100,
            },
            'resets': {
                'max': 3,
                'rewardPerRemaining': 50,
                'rewardForPerfect': 200,
            }
        }
        self.__final_level = 3

    def test_level1(self):
        score = Score({
            'interactions': 'testPositive1,9|testNegative1,2',
            'level': 1,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 35)
        self.assertEqual(score.outcome, Outcomes.Loss.value)

    def test_invalid_level1(self):
        score = Score({
            'interactions': 'testPositive1,11|testNegative1,2',
            'level': 1,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level2(self):
        score = Score({
            'interactions': 'testPositive1,20|testNegative1,5',
            'level': 2,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 175)
        self.assertEqual(score.outcome, Outcomes.Loss.value)

    def test_invalid_level2(self):
        score = Score({
            'interactions': 'testPositive1,31|testNegative1,5',
            'level': 2,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level3(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 3,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 375)
        self.assertEqual(score.outcome, Outcomes.Loss.value)

    def test_invalid_level3(self):
        score = Score({
            'interactions': 'testPositive1,51|testNegative1,5',
            'level': 3,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        with self.assertRaises(InconsistentLevelInteractionException):
            score.compute_score(self.__rulesheet)

    def test_level4(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 4,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 3,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 975)
        self.assertEqual(score.outcome, Outcomes.Win.value)

    def test_above_max_resets(self):
        with self.assertRaises(InvalidResetsException):
            Score({
                'interactions': 'testPositive1,30|testNegative1,5',
                'level': 4,
                'duration': 100,
                'player_id': 1,
                'remainingResets': 4,
            }, self.__final_level, self.__rulesheet.get('resets').get('max'))

    def test_below_zero_resets(self):
        with self.assertRaises(InvalidResetsException):
            Score({
                'interactions': 'testPositive1,30|testNegative1,5',
                'level': 4,
                'duration': 100,
                'player_id': 1,
                'remainingResets': -1,
            }, self.__final_level, self.__rulesheet.get('resets').get('max'))

    def test_under_max_resets(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 4,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 2,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 725)
        self.assertEqual(score.outcome, Outcomes.Win.value)
        self.assertEqual(score.resets_used, self.__rulesheet.get('resets').get('max') - 2)

    def test_zero_resets(self):
        score = Score({
            'interactions': 'testPositive1,30|testNegative1,5',
            'level': 4,
            'duration': 100,
            'player_id': 1,
            'remainingResets': 0,
        }, self.__final_level, self.__rulesheet.get('resets').get('max'))
        self.assertEqual(score.compute_score(self.__rulesheet), 625)
        self.assertEqual(score.outcome, Outcomes.Win.value)
        self.assertEqual(score.resets_used, self.__rulesheet.get('resets').get('max'))

    if __name__ == '__main__':
        unittest.main()
