import os
import json
import dotenv
import psycopg
import redis

from lib.inconsistent_level_interaction_exception import InconsistentLevelInteractionException
from lib.score import Score

dotenv.load_dotenv(dotenv.find_dotenv())


def connect_redis():
    try:
        return redis.Redis(
            host=os.getenv('REDIS_URL'),
            port=int(os.getenv('REDIS_PORT')),
            username=os.getenv('REDIS_USERNAME'),
            password=os.getenv('REDIS_PASSWORD')
        )
    except redis.exceptions.ConnectionError:
        print('Redis connection error')


def load_scores_rule_sheet():
    try:
        with open('rulesheets/turtle-score-sheet.json') as file:
            return json.load(file)
    except FileNotFoundError:
        print('turtle-score-sheet.json not found')


def connect_postgres():
    try:
        connection_string = os.getenv('DATABASE_URL')
        return psycopg.connect(connection_string, autocommit=True)
    except psycopg.OperationalError:
        print('PostgreSQL connection error')


def insert_score_in_db(score: Score, rule_sheet: dict):
    connection = connect_postgres()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO scores (points, level, created_at, player_id, outcome_id, duration) VALUES (%s, %s, %s, %s, %s, %s)",
            (score.compute_score(rule_sheet), score.level, score.timestamp, score.player_id, score.outcome_id, score.duration)
        )


def get_final_level(rule_sheet):
    levels = list(map(
        lambda l: int(l),
        rule_sheet.get('levelRewards').keys()
    ))
    return max(levels)


def main():
    print('Starting up scores cheat detection...')

    redis_client = connect_redis()
    scores_rule_sheet = load_scores_rule_sheet()

    final_level = get_final_level(scores_rule_sheet)

    while True:
        _, new_score = redis_client.brpop('scoreQueue')
        if new_score is not None:
            score = Score(json.loads(new_score), final_level)
            print(f"{score.level}|{score.duration}|{score.player_id}|{score.outcome_id}|{score.timestamp}")
            try:
                computed_points = score.compute_score(scores_rule_sheet)
                print(f"Points computed: {computed_points}")
                insert_score_in_db(score, scores_rule_sheet)
                print("Score inserted successfully")
            except InconsistentLevelInteractionException as e:
                print(e.message)


main()
