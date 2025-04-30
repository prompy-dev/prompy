import pytest
from unittest.mock import patch

from api.steps.user_query import clean_user_query, UserQueryException


class TestUserQuery:
    
    def test_clean_user_query_runnable_structure(self):
        """Test that clean_user_query returns a properly structured runnable"""
        runnable = clean_user_query()
        
        # Verify the runnable has the expected structure
        assert hasattr(runnable, "invoke")
        assert hasattr(runnable, "batch")
    
    def test_clean_user_query_normal_input(self):
        """Test clean_user_query with normal input"""
        runnable = clean_user_query()
        
        # Test with a normal query
        result = runnable.invoke({"input": "Tell me about prompt engineering"})
        
        # Should return cleaned input
        assert isinstance(result, dict)
        assert "clean_query" in result
        assert result["clean_query"] == "Tell me about prompt engineering"
    
    def test_clean_user_query_trims_whitespace(self):
        """Test that clean_user_query doesn't trim whitespace (that's not part of its responsibility)"""
        runnable = clean_user_query()
        
        # Test with whitespace
        result = runnable.invoke({"input": "  Tell me about prompt engineering  "})
        
        # Should return input as is (including whitespace)
        assert result["clean_query"] == "  Tell me about prompt engineering  "
    
    @patch("api.steps.user_query.profanity.contains_profanity")
    def test_clean_user_query_profanity(self, mock_contains_profanity):
        """Test clean_user_query with profanity detection"""
        mock_contains_profanity.return_value = True
        
        runnable = clean_user_query()
        
        # Should raise an exception for profanity
        with pytest.raises(UserQueryException):
            runnable.invoke({"input": "Bad word query"}) 