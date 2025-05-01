import os
import json
import yaml
from typing import Dict, Any
import pathlib
from flask import current_app
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Constants
BASE_DIR = pathlib.Path(__file__).parent.parent
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'system_prompt.yaml')

def load_config() -> tuple[str, Dict[str, Any]]:
    """Load system prompt and variables from YAML config file."""
    with open(CONFIG_PATH) as file:
        config = yaml.safe_load(file)
        return config['prompt'], config.get('variables', {})

def log_response(response: str) -> None:
    """Log the response content for debugging purposes."""
    current_app.logger.debug(response)

def transform_input(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform the input dictionary to expose the right variables to the template.
    
    Args:
        input_dict: Dictionary containing input data
        
    Returns:
        Transformed dictionary with required variables
    """
    transformed = input_dict.copy()
    
    # Add documents from context
    transformed["documents"] = input_dict.get("context", "")
    
    # Extract and normalize score
    if "score_breakdown" in input_dict and "percentage_score" in input_dict["score_breakdown"]:
        transformed["score"] = round(input_dict["score_breakdown"]["percentage_score"] / 10)
    else:
        transformed["score"] = 0
        
    return transformed

def format_llm_response(input_dict: Dict[str, Any], response: str) -> Dict[str, Any]:
    user_query_version_id = input_dict.get("user_query_version_id")
    """
    Format the LLM response into a structured dictionary.
    
    Args:
        input_dict: Original input dictionary
        response: Raw response from LLM
        
    Returns:
        Dictionary containing formatted response data
    """
    try:
        parsed_response = json.loads(response)
    except json.JSONDecodeError:
        current_app.logger.error("Failed to parse LLM response as JSON")
        parsed_response = {
            "strengths": [],
            "improvements": [],
            "tags": []
        }
    
    return {
        "score": input_dict.get("score", 0),
        "strengths": parsed_response.get("strengths", []),
        "improvements": parsed_response.get("improvements", []),
        "tags": parsed_response.get("tags", []),
        "versionId": user_query_version_id
    }

def chat_llm() -> RunnableSequence:
    """
    Create a chat LLM chain for processing and formatting responses.
    
    Returns:
        RunnableSequence combining input transformation and LLM processing
    """
    # Load configuration
    system_prompt, _ = load_config()
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{parsed_response}"),
        ]
    )
    
    # Create processing chain
    def process_response(input_dict: Dict[str, Any]) -> Dict[str, Any]:
        # Format messages
        formatted_prompt = prompt.format_messages(**input_dict)

        # Get LLM response
        response = llm.invoke(formatted_prompt)
        
        # Format and return response
        return format_llm_response(input_dict, response.content)
    
    # Combine transform and processing steps
    transform_step = RunnableLambda(transform_input)
    llm_chain = RunnableLambda(process_response)
    full_chain = transform_step | llm_chain
    
    return full_chain
