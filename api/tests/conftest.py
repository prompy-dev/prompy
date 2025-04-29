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