import json


def get_final_level(rule_sheet):
    levels = list(map(
        lambda l: int(l),
        rule_sheet.get('levelRewards').keys()
    ))
    return max(levels)


def load_scores_rule_sheet():
    try:
        with open('rulesheets/turtle-score-sheet.json') as file:
            return json.load(file)
    except FileNotFoundError:
        print('turtle-score-sheet.json not found')
