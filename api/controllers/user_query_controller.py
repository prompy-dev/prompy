from flask import request, jsonify
from functools import wraps
from better_profanity import profanity

def check_user_query(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    try:
      data = request.get_json()
      user_query = data['prompt']

      # Checks if the user prompt exists
      if user_query is None:
       raise Exception("Missing user prompt")

      if user_query.strip() == "":
        raise Exception("Prompt cannot be empty or only whitespace")

      # Checks if the user prompt is profane
      if profanity.contains_profanity(user_query):
        raise Exception("Profanity is not allowed")

      # Checks if the user prompt is a string
      if not isinstance(user_query, str):
        raise Exception("Invalid user prompt")
        
    except Exception as e:
      return jsonify({
        'success': False,
        'error': str(e)
      }), 400
    else:
      return f(*args, **kwargs)
  return wrapper
