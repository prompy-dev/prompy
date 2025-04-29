# Testing LangChain Runnables in Prompy

This directory contains unit tests for the LangChain runnables used in the Prompy application.

## Test Structure

- `conftest.py`: Contains common pytest fixtures used across test files
- `steps/`: Tests for the runnable components in the `api/steps` directory
  - `test_parse_query.py`: Tests for the parse_query runnable
  - `test_user_query.py`: Tests for the user_query runnable
  - `test_embed_query.py`: Tests for the embed_query runnable
  - `test_chat_llm.py`: Tests for the chat_llm runnable

## Running Tests

To run all tests:

```bash
pytest api/tests
```

To run tests for a specific module:

```bash
pytest api/tests/steps/test_parse_query.py
```

To run tests with verbose output:

```bash
pytest -v api/tests
```

## Testing Approach for LangChain Runnables

1. **Structure Tests**: Verify that the runnable has the expected structure and interfaces.
2. **Mocking External Dependencies**: 
   - Mock LLM calls to avoid actual API requests
   - Use `unittest.mock.patch` to replace external dependencies
3. **Input/Output Tests**: 
   - Test that inputs are properly processed
   - Test that outputs meet expected formats
4. **Exception Handling**: Test error cases and exception handling
5. **Integration Points**: Test how runnables connect to each other

## Tips for Testing LangChain Runnables

### Basic Testing Patterns

- Use `pytest.mark.parametrize` for testing multiple inputs
- Test each component in the runnable chain separately
- Mock LLM responses to test different scenarios
- For complex chains, focus on testing each transformation step

### Advanced Testing Patterns

#### 1. Testing Chain Composition

To test complex chains:

```python
@patch("api.steps.some_module.some_dependency")
def test_complex_chain(mock_dependency):
    # Setup the mock
    mock_dependency.return_value = expected_value
    
    # Create the chain
    chain = your_runnable_chain()
    
    # Test with various inputs
    result = chain.invoke(test_input)
    
    # Assert outputs
    assert result == expected_output
```

#### 2. Contract Testing

Test the input/output "contract" of your runnables:

```python
def test_runnable_contract():
    runnable = your_runnable()
    
    # Test with valid input
    result = runnable.invoke(valid_input)
    assert "expected_key" in result
    assert isinstance(result["expected_key"], ExpectedType)
    
    # Test with invalid input
    with pytest.raises(ExpectedError):
        runnable.invoke(invalid_input)
```

#### 3. Using Functional Tests

For testing end-to-end behavior with controlled inputs/outputs:

```python
class TestRunnableFunctional:
    def setup_method(self):
        # Setup a mock LLM that returns predefined responses
        self.patched_llm = patch("api.steps.module.llm").start()
        self.patched_llm.invoke.side_effect = self._mock_llm_responses
        
    def teardown_method(self):
        patch.stopall()
        
    def _mock_llm_responses(self, messages):
        # Return different responses based on input
        if "query1" in str(messages):
            return "response1"
        return "default response"
        
    def test_end_to_end(self):
        # Test the full chain with controlled inputs
        result = your_full_chain.invoke({"input": "query1"})
        assert result["output"] == "expected output"
```

#### 4. Snapshot Testing

For testing outputs that are expected to remain stable:

```python
def test_output_snapshot(snapshot):
    runnable = your_runnable()
    result = runnable.invoke(test_input)
    snapshot.assert_match(json.dumps(result, sort_keys=True), "expected_output.json")
```

#### 5. Integration Testing with Tracing

For observing the flow through a complex chain:

```python
from langchain.callbacks.tracers import ConsoleCallbackHandler

def test_chain_flow():
    # Setup callback for tracing
    callbacks = [ConsoleCallbackHandler()]
    
    # Run chain with tracing
    runnable = your_runnable()
    result = runnable.invoke(test_input, config={"callbacks": callbacks})
    
    # Assert on final output
    assert result == expected_output
```

## Next Steps

To expand the test suite:

1. Add more comprehensive tests for each runnable
2. Implement integration tests between connected runnables
3. Add performance testing for critical chains
4. Create fixtures that simulate realistic user inputs 