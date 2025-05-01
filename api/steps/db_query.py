import os
from flask import current_app
from langchain_core.runnables import RunnableLambda
from langchain_community.utilities import SQLDatabase
from sqlalchemy import text

db = SQLDatabase.from_uri(os.environ.get("SUPABASE_URI"))

user_query_template = """
  INSERT INTO user_query(
    created_by
  ) VALUES (
    '{created_by}'
  ) RETURNING id;
"""

user_query_version_template = """
    INSERT INTO user_query_version(
        user_query,
        task,
        role,
        context,
        rules,
        examples,
        format,
        user_query_id
    ) VALUES (
        '{user_query}',
        {task},
        {role},
        {context},
        {rules},
        {examples},
        {format},
        {user_query_id}
    ) RETURNING id;
"""

scores_insert_template = """
  INSERT INTO scores (
      total_score,
      max_possible_score,
      percentage_score,
      task_score,
      role_score,
      context_score,
      rules_score,
      examples_score,
      format_score,
      word_count_score,
      user_query_version_id
  ) VALUES (
      {total_score},
      {max_possible_score},
      {percentage_score},
      {task_score},
      {role_score},
      {context_score},
      {rules_score},
      {examples_score},
      {format_score},
      {word_count_score},
      {user_query_version_id}
  ) RETURNING id;
"""


def insert_user_query(query: dict, connection):
    try:
        sql = user_query_template.format(created_by=query.get("created_by"))
        result = connection.execute(text(sql))
        return result.scalar() 
    except Exception as e:
        raise Exception("Failed to insert into user_query table: " + str(e))


def insert_user_query_version(query: dict, connection, user_query_id):
    try:
        sql = user_query_version_template.format(
            user_query=query.get("user_query"),
            task=str(query.get("task")),
            role=str(query.get("role")),
            context=str(query.get("context")),
            rules=str(query.get("rules")),
            examples=str(query.get("examples")),
            format=str(query.get("format")),
            user_query_id=user_query_id,
        )
        result = connection.execute(text(sql))
        return result.scalar() 
    except Exception as e:
        raise Exception("Failed to insert into user_query_version table: " + str(e))


def insert_scores_query(query: dict, connection, user_query_version_id):
    score_by_field = query.get("score_by_field")
    try:
        sql = scores_insert_template.format(
            total_score=query.get("total_score"),
            max_possible_score=str(query.get("max_possible_score")),
            percentage_score=str(query.get("percentage_score")),
            task_score=str(score_by_field.get("task")),
            role_score=str(score_by_field.get("role")),
            context_score=str(score_by_field.get("context")),
            rules_score=str(score_by_field.get("rules")),
            examples_score=str(score_by_field.get("examples")),
            format_score=str(score_by_field.get("format")),
            word_count_score=str(score_by_field.get("word_count")),
            user_query_version_id=user_query_version_id,
        )
        result = connection.execute(text(sql))
        return result.scalar()  
    except Exception as e:
        raise Exception("Failed to insert into scores table: " + str(e))


def run_query() -> RunnableLambda:
    return RunnableLambda(lambda input: _run_query(input))


def _run_query(d: dict):
    connection = db._engine.connect()
    transaction = connection.begin()

    try:
        parsed_response = d.get("parsed_response")
        score_breakdown = d.get("score_breakdown")

        user_query_id = insert_user_query(
            query={"created_by": "Prompy"}, connection=connection
        )

        user_query_version_id = insert_user_query_version(
            query=parsed_response,
            connection=connection,
            user_query_id=user_query_id,
        )

        insert_scores_query(
            query=score_breakdown,
            connection=connection,
            user_query_version_id=user_query_version_id,
        )

        d["user_query_version_id"] = user_query_version_id

        transaction.commit()
        return d

    except Exception as e:
        transaction.rollback()
        current_app.logger.exception(e)
        raise Exception("Failed inserting into db: " + str(e))
    finally:
        connection.close()
