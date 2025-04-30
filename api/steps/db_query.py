import os
import asyncio
import asyncpg
from langchain_core.runnables import RunnableLambda
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(os.environ.get("SUPABASE_URI"))


async def get_connection(connection_string: str):
    return await asyncpg.connect(connection_string)


user_query_insert_template = """
INSERT INTO user_query (
    user_query,
    task,
    role,
    context,
    rules,
    examples,
    format
) VALUES (
    '{user_query}',
    {task},
    {role},
    {context},
    {rules},
    {examples},
    {format}
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
    user_query_id
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
    {user_query_id}
);
"""


async def execute_insert_query(db, query, params):
    formatted_query = query.format(**params)
    await db.execute(formatted_query)


def db_query() -> RunnableLambda:
    return RunnableLambda(lambda input: _db(input))


async def _db(d: dict):
    # score_breakdown = d.get("score_breakdown")
    parsed_response = d.get("parsed_response")

    # if score_breakdown is None and parsed_response is None:
    #     raise Exception("dbQueryException: Failed to send query to db")

    # fire and forget db query so we don't block the pipeline
    await execute_insert_query(db=db, query=user_query_insert_template, params=parsed_response)

    return {"parsed_response": parsed_response}
