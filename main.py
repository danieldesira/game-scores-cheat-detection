import os
import json
import dotenv
import psycopg
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


def connect_postgres():
    connection_string = os.getenv('DATABASE_URL')
    return psycopg.connect(connection_string, autocommit=True)


def remove_scores_from_db(ids: list[int]):
    if len(ids) > 0:
        connection = connect_postgres()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM scores WHERE id IN (%s)", ids)


def main():
    scores_to_review = load_redis_scores()
    scores_sheet = load_scores_sheet()

    offending_score_ids = list()

    for score_entry in scores_to_review:
        score = Score(score_entry)
        if score.check(scores_sheet):
            print(f"Score {score.id} verified successfully")
        else:
            print(f"Cheat score detected. id: {score.id} |"
                  f" {score.points} points | level {score.level} | duration {score.duration} |"
                  f" {score.outcome_id} | {score.player_id}")
            offending_score_ids.append(score.id)

    remove_scores_from_db(offending_score_ids)
    save_pending_scores([])


main()
