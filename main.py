import os
import json
import dotenv
import redis
from score import Score

dotenv.load_dotenv(dotenv.find_dotenv())


def connect_redis():
    return redis.Redis(
        host=os.getenv('REDIS_URL'),
        port=int(os.getenv('REDIS_PORT')),
        username=os.getenv('REDIS_USERNAME'),
        password=os.getenv('REDIS_PASSWORD')
    )


def load_redis_scores():
    redis_client = connect_redis()
    data = redis_client.get('scores')
    return json.loads(data)


def load_scores_sheet():
    try:
        with open('turtle-score-sheet.json') as file:
            return json.load(file)
    except FileNotFoundError:
        print('turtle-score-sheet.json not found')


def save_pending_scores(scores):
    redis_client = connect_redis()
    redis_client.set('scores', json.dumps(scores))


def main():
    scores_to_review = load_redis_scores()
    scores_sheet = load_scores_sheet()

    for score_entry in scores_to_review:
        score = Score(score_entry)
        ok = score.check(scores_sheet)
        if ok:
            print(f"Score {score.id} verified successfully")
        else:
            print(f"Possible cheat score detected. id: {score.id} |"
                  f" {score.points} points | level {score.level} | duration {score.duration} |"
                  f" {score.outcome_id} | {score.player_id}")

    save_pending_scores([])


main()
