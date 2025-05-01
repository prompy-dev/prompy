import pytest

from api.steps.summarize_query import summarize_query


class TestSummarizeQuery:
        
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
        assert "The query is missing the following important elements:\ncontext,  rules,  examples,  format,  " in result["summary"]
        assert "The query contains the following elements:\n- task\n- role" in result["summary"]
        assert "task" in result["summary"]
        assert "role" in result["summary"]
        assert "context" in result["summary"]
        assert "rules" in result["summary"]
   
   
    def test_summarize_query_without_parsed_response(self):
      """Test summarize_query without a parsed response"""
      runnable = summarize_query()

          # Should raise an exception for missing parsed_response
      with pytest.raises(Exception) as e:
        runnable.invoke({})
      assert str(e.value) == "SummarizeQueryException: Missing 'parsed_response' in input dictionary"
 
    def test_summarize_query_with_missing_user_query(self):
      """Test summarize_query with a missing user query"""
      runnable = summarize_query()
      
      # Mock input dictionary without user_query
      mock_input = {
        "parsed_response": {}}    
        
        # Should raise an exception for missing user_query
      with pytest.raises(Exception) as e:
        runnable.invoke(mock_input)
      assert str(e.value) == "SummarizeQueryException: Missing 'user_query' in parsed_response"
