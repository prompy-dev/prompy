import pytest
from unittest.mock import patch, MagicMock
import json
from langchain_core.runnables import RunnableLambda

from api.steps.score_query import score_query, get_word_count_score


@pytest.fixture
def sample_parsed_query():
    return {
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


class TestScoreQuery:
    
    def test_get_word_count_score(self):
        """Test the word count scoring function"""
        # Test ideal word count range
        assert get_word_count_score(150, 3) == 3
        
        # Test below minimum ideal word count
        assert get_word_count_score(50, 3) == 1.5  # 50/100 * 3
        
        # Test above maximum ideal word count
        assert get_word_count_score(600, 3) == 1.5  # 300/600 * 3
    
    def test_score_query_functionality(self, sample_parsed_query, expected_score_output):
        """Test that score_query correctly scores the input"""
        from flask import Flask
        
        app = Flask(__name__)
        with app.app_context():
            runnable = score_query()
            
            # Execute the runnable with the sample query
            result = runnable.invoke(sample_parsed_query)
            
            # Verify score components are present
            assert "score_breakdown" in result
            assert "parsed_response" in result
            
            # Verify score breakdown structure
            assert "total_score" in result["score_breakdown"]
            assert "max_possible_score" in result["score_breakdown"]
            assert "percentage_score" in result["score_breakdown"]
            assert "score_by_field" in result["score_breakdown"]
            
            # Verify calculated scores match expected values
            assert result["score_breakdown"]["total_score"] == expected_score_output["score_breakdown"]["total_score"]
            assert result["score_breakdown"]["max_possible_score"] == expected_score_output["score_breakdown"]["max_possible_score"]
            assert result["score_breakdown"]["percentage_score"] == expected_score_output["score_breakdown"]["percentage_score"] 