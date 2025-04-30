from api.steps.chat_llm import chat_llm

class TestChatLLM:
    
    def test_chat_llm_output_structure(self, expected_score_output):
        """Test that chat_llm returns a properly structured output"""
        runnable = chat_llm()
        
        # Execute the runnable with the sample output
        result = runnable.invoke(expected_score_output)
        
        assert 'strengths' in result
        assert 'improvements' in result
        assert 'tags' in result
        