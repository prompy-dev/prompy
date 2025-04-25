from better_profanity import profanity
from langchain_core.runnables import RunnableLambda


class UserQueryException(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"UserQueryException: {self.message}"


def clean_user_query() -> RunnableLambda:
    return RunnableLambda(lambda input: _clean_query(input))


def _clean_query(d: dict):
    user_query = d.get("input")

    if user_query is None:
        raise UserQueryException("Missing user prompt")

    if user_query.strip() == "":
        raise UserQueryException("Prompt cannot be empty or only whitespace")

    # Checks if the user prompt is profane
    if profanity.contains_profanity(user_query):
        raise UserQueryException("Profanity is not allowed")

    # Checks if the user prompt is a string
    if not isinstance(user_query, str):
        raise UserQueryException("Invalid user prompt")

    return {"clean_query": user_query}
