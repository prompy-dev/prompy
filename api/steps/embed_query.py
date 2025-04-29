import os
from flask import current_app
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableLambda


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=os.environ.get("OPEN_API_KEY")
)


def log_repsonse(res):
    current_app.logger.debug(res)


def embed_query() -> RunnableLambda:
    return RunnableLambda(lambda input: _embed(input))


def _embed(d: dict):
    try:
        parsed_response = d.get("parsed_response")
        summary = d.get("summary")

        if "user_query" not in parsed_response:
            raise Exception("EmbedUserQueryException")

        vector = embeddings.embed_query(summary)

        d["embedding"] = vector

        return d
    except:
        raise Exception("EmbedUserQueryException")
