from langchain_core.runnables import RunnableLambda
from flask import current_app

def log_response(res):
    current_app.logger.debug(res)

def _construct_summary(parsed_response: dict) -> str:
    """Constructs a natural language summary from the parsed response."""
    if not isinstance(parsed_response, dict):
        raise Exception(f"Expected dict, got {type(parsed_response)}")
    
    user_query = parsed_response.get("user_query", "")
    if not user_query:
        raise Exception("Missing user_query in parsed response")
    
    present_elements = []
    missing_elements = []
    
    # Check each element
    elements = {
        "task": "task",
        "role": "role",
        "context": "context",
        "rules": "rules",
        "examples": "examples",
        "format": "format"
    }
    
    for key, label in elements.items():
        if parsed_response.get(key, False):
            present_elements.append(label)
        else:
            missing_elements.append(label)
    
    # Construct the summary
    summary = f"The user query is: {user_query}\n\n"
    
    if present_elements:
        summary += "The query contains the following elements:\n"
        for element in present_elements:
            summary += f"- {element}\n"
    
    if missing_elements:
        summary += "\nThe query is missing the following important elements:\n"
        for element in missing_elements:
            summary += f"{element},  "
    
    return summary

def summarize_query() -> RunnableLambda:
    return RunnableLambda(lambda input: _summarize(input))

def _summarize(d: dict):
    try:
        if not isinstance(d, dict):
            raise Exception(f"Expected dict input, got {type(d)}")
            
        parsed_response = d.get("parsed_response")
        if parsed_response is None:
            raise Exception("Missing 'parsed_response' in input dictionary")
            
        if not isinstance(parsed_response, dict):
            raise Exception(f"Expected parsed_response to be dict, got {type(parsed_response)}")

        if "user_query" not in parsed_response:
            raise Exception("Missing 'user_query' in parsed_response")

        summary = _construct_summary(parsed_response)
        
    except Exception as e:
        raise Exception(f"SummarizeQueryException: {str(e)}")
    else:
        log_response(summary)
        return {"summary": summary, "parsed_response": parsed_response}