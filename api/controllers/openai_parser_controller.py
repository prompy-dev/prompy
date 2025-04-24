from flask import request, g, jsonify
from app.services.OpenAIClient import OpenAIChatClient, OpenAIClientException
from functools import wraps

chat_client = OpenAIChatClient(model='gpt-4o', config={
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 256,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
}, prediction={
  "type": "content",
  "content": """
    class ParsedUserQuery {
      userQuery: string = "";
      task: boolean = false;
      role: boolean = false;
      context: boolean = false;
      rules: boolean = false;
      examples: boolean = false;
      format: boolean = false;
    }
    """
})

system_prompt = """
You will return a JSON object with the following attributes:
- user_query: The original user query.
- task: boolean (true if the user query contains a task, false otherwise)
- role: boolean (true if a role is identified in the user query, false otherwise)
- context: boolean (true if a context is identified in the user query, false otherwise)
- rules: boolean (true if rules have been identified in the user query, false otherwise)
- examples: boolean (true if examples are present in the user query, false otherwise)
- format: boolean (true if a response format has been identified in the user query, false otherwise)

You should always respond in JSON format.
"""

chat_client.set_system_prompt(
  prompt=system_prompt
)


def openai_parser(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    try:
      data = request.get_json()
      user_query = data['prompt']

      parsed_user_query_response = chat_client.create(user_prompt=user_query)

      print('PARSED USER QUERY ========', parsed_user_query_response)

      if parsed_user_query_response is None:
        raise Exception("parsed user query response is not available")
      
      if not isinstance(parsed_user_query_response, dict):
        raise Exception("parsed user query response is not a dictionary")

      g.parsed_user_query = parsed_user_query_response

      return f(*args, **kwargs)
    except Exception as e:
      return jsonify({
        'success': False,
        'error': str(e)
      }), 400
  return wrapper