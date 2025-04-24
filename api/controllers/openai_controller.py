from flask import request, g, jsonify
from app.services.OpenAIClient import OpenAIChatClient, OpenAIClientException
from functools import wraps

chat_client = OpenAIChatClient(model='gpt-4o', config={
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 256,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
})

chat_client.set_system_prompt(
  prompt='You are my best friend'
)

def openai_chat(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    try:
      data = request.get_json()
      user_query = data['prompt']

      if not user_query or not isinstance(user_query, str):
        raise Exception("Invalid user prompt")

      chat_response = chat_client.create(user_prompt=user_query)
    except OpenAIClientException as e:
      return jsonify({
        'success': False,
        'error': e.message
      })
    else:
      print('USER QUERY ========', user_query)
      g.user_prompt = user_query
      g.chat_response = chat_response
      return f(*args, **kwargs)
  return wrapper