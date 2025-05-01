import pytest
import json
from api.steps.parse_query import parse_query


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
        "format": False,
        "word_count": 8
    })


class TestParseQuery:
        
    def test_parse_query_with_valid_input(self, sample_query, sample_json_response):
        """Test parse_query with valid input"""
        runnable = parse_query()
        
        # Execute the runnable with the sample query
        result = runnable.invoke(sample_query)
        
        # Verify the result matches the expected dictionary structure
        assert result == {"parsed_response": json.loads(sample_json_response)}
        
    def test_parse_query_with_missing_clean_query(self):
        """Test parse_query with a missing clean query"""
        runnable = parse_query()
        
        # Should raise an exception for missing user_query
        with pytest.raises(Exception) as e:
            runnable.invoke({})
            assert str(e.value) == "SummarizeQueryException: parsed user query response is not available"