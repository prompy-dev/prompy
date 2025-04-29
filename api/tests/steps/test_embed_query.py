import pytest
from unittest.mock import patch, MagicMock
from langchain_core.runnables import RunnableLambda

from api.steps.embed_query import embed_query


class TestEmbedQuery:
    
    def test_embed_query_runnable_structure(self):
        """Test that embed_query returns a properly structured runnable"""
        runnable = embed_query()
        
        # Verify the runnable has the expected structure
        assert hasattr(runnable, "invoke")
        assert hasattr(runnable, "batch")
        assert isinstance(runnable, RunnableLambda) 