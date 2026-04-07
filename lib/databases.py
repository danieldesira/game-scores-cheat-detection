import os

import psycopg
import redis

from lib.score import Score


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
            "INSERT INTO scores (points, level, created_at, player_id, outcome, duration, resets_used) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (score.compute_score(rule_sheet), score.level, score.timestamp, score.player_id, score.outcome,
             score.duration, score.resets_used)
        )
