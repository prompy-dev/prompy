import json
import os
from flask import current_app
from langchain_core.runnables import RunnableLambda
from sqlalchemy import text
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(os.environ.get("SUPABASE_URI"))

query_feedback_template = """
    INSERT INTO feedback_response (
      improvements,
      score,
      strengths,
      tags,
      user_query_version_id
  ) VALUES (
      ARRAY{improvements}::TEXT[],
      {score},
      ARRAY{strengths}::TEXT[],
      ARRAY{tags}::TEXT[],
      {user_query_version_id}
  );
"""


def query_feedback():
    return RunnableLambda(lambda input: insert_response(response=input))


def format_query(template: str, data: dict, user_query_version_id: int = 1) -> str:
    def to_sql_array(values):
        escaped_values = []
        for v in values:
            escaped = v.replace("'", "''")  # Escape single quotes
            escaped_values.append(f"'{escaped}'")
        return f"[{', '.join(escaped_values)}]"

    improvements = to_sql_array(data["improvements"])
    strengths = to_sql_array(data["strengths"])
    tags = to_sql_array(data["tags"])
    score = data["score"]

    return template.format(
        improvements=improvements,
        strengths=strengths,
        tags=tags,
        score=score,
        user_query_version_id=user_query_version_id,
    )


def insert_response(response: dict):
    version_id = response.pop("versionId")
    query = format_query(
        template=query_feedback_template,
        data=response,
        user_query_version_id=version_id,
    )

    connection = db._engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(text(query))
        transaction.commit()
    except Exception as e:
        current_app.logger.exception(e)
        transaction.rollback()
        raise Exception("Failed to insert into response table:")
    finally:
        connection.close()

    return response
