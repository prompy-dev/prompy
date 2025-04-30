import ast
import json
import os
import asyncio

from flask import current_app
import asyncpg
from langchain_core.runnables import RunnableLambda
from langchain_community.utilities import SQLDatabase

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

def insert_user_query(query: dict, db):
  try:
    query = user_query_template.format(
       created_by=query.get("created_by")
    )
    return db.run(query)
  except Exception as e:
    raise Exception('Failed to insert into user_query table '+ str(e))

def insert_user_query_version(query: dict, db, user_query_id):
  try:
    query = user_query_version_template.format(
        user_query=query.get('user_query'),
        task=str(query.get("task")),
        role=str(query.get("role")),
        context=str(query.get("context")),
        rules=str(query.get("rules")),
        examples=str(query.get("examples")),
        format=str(query.get("format")),
        user_query_id=user_query_id

    )
    return db.run(query)
  except Exception as e:
    raise Exception('Failed to insert into user_query_version table '  + str(e))
  

# {"total_score": 16.25, "max_possible_score": 19, "percentage_score": 73.86363636363636, "score_by_field": {"task": 4, "role": 3, "context": 2, "rules": 3, "examples": 0, "format": 2, "word_count": 2.25}}
    
def insert_scores_query(query: dict, db, user_query_version_id):
  score_by_field = query.get("score_by_field")
  try:
    query = scores_insert_template.format(
        total_score=query.get('total_score'),
        max_possible_score=str(query.get("max_possible_score")),
        percentage_score=str(query.get("percentage_score")),
        task_score=str(score_by_field.get("task")),
        role_score=str(score_by_field.get("role")),
        context_score=str(score_by_field.get("context")),
        rules_score=str(score_by_field.get("rules")),
        examples_score=str(score_by_field.get("examples")),
        format_score=str(score_by_field.get("format")),
        word_count_score=str(score_by_field.get("word_count")),
        user_query_version_id=user_query_version_id
    )
    return db.run(query)
  except Exception as e:
    raise Exception('Failed to insert into scores table ' + str(e))

def get_created_id(id):
  return (((ast.literal_eval(id))[0])[0])

def run_query() -> RunnableLambda:
   return RunnableLambda(lambda input: _run_query(input))

def _run_query(d: dict):
  parsed_response = d.get("parsed_response")
  score_breakdown = d.get("score_breakdown")

  current_app.logger.debug(json.dumps(parsed_response))
  current_app.logger.debug(json.dumps(score_breakdown))

  user_query_id = insert_user_query(query={"created_by": "Prompy"}, db=db)
  current_app.logger.debug('*******************')
  current_app.logger.debug(get_created_id(user_query_id))
  current_app.logger.debug('*******************')
  user_query_version_id = insert_user_query_version(query=parsed_response, db=db, user_query_id=get_created_id(user_query_id))
  insert_scores_query(query=score_breakdown, db=db, user_query_version_id=get_created_id(user_query_version_id))


  current_app.logger.debug(db.get_usable_table_names())

  return d

