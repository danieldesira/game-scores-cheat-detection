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


def load_scores_rule_sheet():
    try:
        with open('turtle-score-sheet.json') as file:
            return json.load(file)
    except FileNotFoundError:
        print('turtle-score-sheet.json not found')


def connect_postgres():
    connection_string = os.getenv('DATABASE_URL')
    return psycopg.connect(connection_string, autocommit=True)


def remove_score_from_db(score_id: int):
    connection = connect_postgres()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM scores WHERE id = %s", (score_id,))


def main():
    print('Starting up scores cheat detection...')

    redis_client = connect_redis()
    scores_rule_sheet = load_scores_rule_sheet()

    while True:
        _, new_score = redis_client.brpop('scoreQueue')
        if new_score is not None:
            score = Score(json.loads(new_score))
            if score.check(scores_rule_sheet):
                print(f"Score {score.id} verified successfully")
            else:
                print(f"Cheat score detected. id: {score.id} |"
                      f" {score.points} points | level {score.level} | duration {score.duration} |"
                      f" {score.outcome_id} | {score.player_id}")
                remove_score_from_db(score.id)


main()
