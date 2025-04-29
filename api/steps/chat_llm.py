import os
import yaml
from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

# Load system prompt from YAML
with open('../config/system_prompt.yaml') as file:
    config = yaml.safe_load(file)
    system_prompt = config['prompt']
    variables = config.get('variables', {})

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def chat_llm(score: int, documents: list[str]) -> RunnableSequence:
    prompt = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{parsed_response}"),
        ]
    )

    # Create a chain that includes the variables
    chain = prompt | llm | StrOutputParser()
    
    # Add variables to the chain with the provided score and documents
    chain = chain.with_config({
        "configurable": {
            "variables": {
                **variables,
                "score": score,
                "documents": documents
            }
        }
    })
    
    return chain
