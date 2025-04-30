import pytest
from unittest.mock import patch, MagicMock
from langchain_core.runnables import RunnableSequence

from api.steps.chat_llm import chat_llm


class TestChatLLM:
    
    def test_chat_llm_runnable_structure(self):
        """Test that chat_llm returns a properly structured runnable"""
        runnable = chat_llm()
        
        # Verify the runnable has the expected structure
        assert hasattr(runnable, "invoke")
        assert hasattr(runnable, "batch")
        assert isinstance(runnable, RunnableSequence) 