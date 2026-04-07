import json
import dotenv

from lib.databases import connect_redis, insert_score_in_db
from lib.inconsistent_level_interaction_exception import InconsistentLevelInteractionException
from lib.rulesheet_utils import get_final_level, load_scores_rule_sheet
from lib.score import Score

dotenv.load_dotenv(dotenv.find_dotenv())

print('Starting up scores cheat detection...')

redis_client = connect_redis()
scores_rule_sheet = load_scores_rule_sheet()

final_level = get_final_level(scores_rule_sheet)
max_resets = scores_rule_sheet.get('resets').get('max')

while True:
    _, new_score = redis_client.brpop('scoreQueue')
    if new_score is not None:
        score = Score(json.loads(new_score), final_level, max_resets)
        print(
            f"{score.level}|{score.duration}|{score.player_id}|{score.outcome}|{score.timestamp}|{score.remaining_resets}")
        try:
            computed_points = score.compute_score(scores_rule_sheet)
            print(f"Points computed: {computed_points}")
            insert_score_in_db(score, scores_rule_sheet)
            print("Score inserted successfully")
        except InconsistentLevelInteractionException as e:
            print(e.message)
