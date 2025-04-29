import os
import yaml
from langchain_openai import ChatOpenAI
import pathlib
from langchain_core.runnables import RunnableLambda

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

# Get absolute path to config directory
base_dir = pathlib.Path(__file__).parent.parent
config_path = os.path.join(base_dir, 'config', 'system_prompt.yaml')

# Load system prompt from YAML
with open(config_path) as file:
    config = yaml.safe_load(file)
    system_prompt = config['prompt']
    variables = config.get('variables', {})

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def transform_input(input_dict):
    """Transform the input dictionary to expose the right variables to the template."""
    # Create a copy so we don't modify the original
    transformed = input_dict.copy()
    
    # Add the needed variables
    transformed["documents"] = input_dict.get("context", "")
    
    # Extract score from score_breakdown
    if "score_breakdown" in input_dict and "percentage_score" in input_dict["score_breakdown"]:
        transformed["score"] = round(input_dict["score_breakdown"]["percentage_score"] / 10)
    else:
        transformed["score"] = 0
        
    return transformed

def chat_llm() -> RunnableSequence:
    # First transform the input to have the right variables
    transform_step = RunnableLambda(transform_input)
    
    prompt = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{parsed_response}"),
        ]
    )

    # Create a chain
    llm_chain = prompt | llm | StrOutputParser()
    
    # Combine transform and llm chain
    full_chain = transform_step | llm_chain
    
    return full_chain
