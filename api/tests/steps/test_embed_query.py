import pytest
from langchain_core.runnables import RunnableLambda

from api.steps.embed_query import embed_query

@pytest.fixture
def sample_dict():
    return {
        "parsed_response": {
            "user_query": "What is a good prompt for summarizing text?"
        },
        "summary": "What is a good prompt for summarizing text?"
    }

class TestEmbedQuery:
        
    def test_embed_query_with_missing_user_query(self):
        """Test embed_query with a missing parsed_response"""
        runnable = embed_query()
        
        # Should raise an exception for missing parsed_response     
        with pytest.raises(Exception) as e:
            runnable.invoke({
                "parsed_response": {}
            })
            assert str(e.value) == "SummarizeQueryException: EmbedUserQueryException"

    def test_embed_query_with_valid_input(self, sample_dict):
        """Test embed_query with valid input"""
        runnable = embed_query()
        
        # Execute the runnable with the sample query
        result = runnable.invoke(sample_dict)
        
        # Verify the result matches the expected dictionary structure
        assert "embedding" in result
