import os
from flask import current_app
import json
from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser


llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.environ.get("OPEN_API_KEY"),
    top_p=1.0,
    # prediction ?
)

code = """
  {{
    "user_uery": string;
    "task": boolean;
    "role": boolean;
    "context": boolean;
    "rules": boolean;
    "examples": boolean;
    "format": boolean;
  }}
"""

system_prompt = f"""
    You will return a JSON object with the following attributes:
    - user_query: The original user query.
    - task: boolean (true if the user query contains a task, false otherwise)
    - role: boolean (true if a role is identified in the user query, false otherwise)
    - context: boolean (true if a context is identified in the user query, false otherwise)
    - rules: boolean (true if rules have been identified in the user query, false otherwise)
    - examples: boolean (true if examples are present in the user query, false otherwise)
    - format: boolean (true if a response format has been identified in the user query, false otherwise)
    - Do not wrap the json in functions like \`\`\`json(...)\`\`\`

    You should always respond in JSON format:
      {code}
"""


class ParseUserQueryException(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ParseUserQueryException: {self.message}"


def handle_exception(d: dict):
    parse_response = d.get("parsed_response")

    if parse_response is None:
        raise ParseUserQueryException("parsed user query response is not available")

    return {"parsed_response": parse_response}


def log_repsonse(res):
    current_app.logger.debug("ParseUserQuery", res)


def handle_response(chat_response):
    log_repsonse(chat_response)
    parsed_response = json.loads(chat_response)
    return {"parsed_response": parsed_response}


def parse_query() -> RunnableSequence:
    prompt = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{clean_query}"),
        ]
    )

    return (
        prompt
        | llm
        | StrOutputParser()
        | RunnableLambda(lambda chat_response: handle_response(chat_response))
        | RunnableLambda(lambda query: handle_exception(query))
    )
