import pytest
from unittest.mock import patch

from api.steps.summarize_query import summarize_query


class TestSummarizeQuery:
    
    def test_summarize_query_runnable_structure(self):
        """Test that summarize_query returns a properly structured runnable"""
        runnable = summarize_query()
        
        # Verify the runnable has the expected structure
        assert hasattr(runnable, "invoke")
        assert hasattr(runnable, "batch")
        
    def test_summarize_query_with_parsed_response(self):
        """Test summarize_query with a mocked parsed response"""
        runnable = summarize_query()
        
        # Mock input dictionary with parsed_response
        mock_input = {
            "parsed_response": {
                "user_query": "Help me write a prompt",
                "task": "Write a prompt",
                "role": "prompt engineer",
                "context": None,
                "rules": None,
                "examples": None,
                "format": None
            }
        }
        
        # Run the summarize query
        result = runnable.invoke(mock_input)
        
        # Verify the summary was added to the dictionary
        assert "summary" in result
        assert isinstance(result["summary"], str)
        assert "The user query is: Help me write a prompt" in result["summary"]
        assert "task" in result["summary"]
        assert "role" in result["summary"]
        assert "context" in result["summary"]
        assert "rules" in result["summary"]
   