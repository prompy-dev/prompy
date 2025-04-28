import os
import yaml
from pathlib import Path
from flask import request, g, jsonify
from app.services.OpenAIClient import OpenAIChatClient, OpenAIClientException
from functools import wraps

# Get the absolute path to the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
SYSTEM_PROMPT_PATH = PROJECT_ROOT / 'api' / 'config' / 'system_prompt.yaml'

chat_client = OpenAIChatClient(model='gpt-4o', config={
  "temperature": 0.7,
  "top_p": 1.0,
  "max_tokens": 256,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
})

try:
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        system_prompt = config['prompt']
    chat_client.set_system_prompt(prompt=system_prompt)
except FileNotFoundError:
    raise RuntimeError(f"System prompt file not found at {SYSTEM_PROMPT_PATH}")
except yaml.YAMLError as e:
    raise RuntimeError(f"Error parsing YAML configuration: {str(e)}")
except Exception as e:
    raise RuntimeError(f"Error reading system prompt: {str(e)}")

def prompy_system_test(f):
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
