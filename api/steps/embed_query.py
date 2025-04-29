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

        if "user_query" not in parsed_response:
            raise Exception("EmbedUserQueryException")

        q = parsed_response.get("user_query")

        vector = embeddings.embed_query(q)
    except:
        raise Exception("EmbedUserQueryException")
    else:
        log_repsonse(vector)
        return {"embedding": vector, "parsed_response": parsed_response}
