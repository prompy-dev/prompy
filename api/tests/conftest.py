import pytest
from unittest.mock import MagicMock
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


@pytest.fixture
def mock_llm():
    """Fixture to create a mock LLM for testing"""
    mock = MagicMock(spec=ChatOpenAI)
    return mock


@pytest.fixture
def str_output_parser():
    """Fixture to provide a StrOutputParser"""
    return StrOutputParser() 

@pytest.fixture
def expected_score_output():
    return {
        "score_breakdown": {
            "total_score": 13,
            "max_possible_score": 19,
            "percentage_score": 59.09090909090909,
            "score_by_field": {
                "task": 4,
                "role": 3,
                "context": 0,
                "rules": 3,
                "examples": 0,
                "format": 0,
                "word_count": 3
            }
        },
        "parsed_response": {
            "user_query": "Create a prompt that helps summarize scientific papers",
            "task": True,
            "role": True,
            "context": False,
            "rules": True,
            "examples": False,
            "format": False,
            "word_count": 150
        }
    }