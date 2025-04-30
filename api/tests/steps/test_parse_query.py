import pytest
from unittest.mock import patch, MagicMock
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableSequence

from api.steps.parse_query import parse_query, ParseUserQueryException


@pytest.fixture
def sample_query():
    return {"clean_query": "What is a good prompt for summarizing text?"}


@pytest.fixture
def sample_json_response():
    return json.dumps({
        "user_query": "What is a good prompt for summarizing text?",
        "task": True,
        "role": False,
        "context": False,
        "rules": False, 
        "examples": False,
        "format": False
    })


class TestParseQuery:
    
    def test_parse_query_runnable_structure(self):
        """Test that parse_query returns a properly structured runnable"""
        runnable = parse_query()
        
        # Verify the runnable has the expected structure
        assert hasattr(runnable, "invoke")
        assert hasattr(runnable, "batch")
        assert isinstance(runnable, RunnableSequence)