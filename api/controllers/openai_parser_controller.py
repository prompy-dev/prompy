from flask import request, g, jsonify
from functools import wraps
import json
from openai import OpenAI
client = OpenAI()

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

code = """
class UserQuery {
  userQuery: string = "";
  task: boolean = false;
  role: boolean = false;
  context: boolean = false;
  rules: boolean = false;
  examples: boolean = false;
  format: boolean = false;
}

export default UserQuery;
"""


def openai_parser(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    try:
      data = request.get_json()
      user_query = data['prompt']

      completion = client.chat.completions.create(
          model="gpt-4.1",
          messages=[
              {
                  "role": "system",
                  "content": system_prompt
              },
              {
                  "role": "user",
                  "content": user_query
              }
          ],
          prediction={
              "type": "content",
              "content": code
          }
      )
      print(completion.choices[0].message.content)

      parsed_data = completion.choices[0].message.content

      # Parse the JSON string into a Python dictionary
      parsed_data = json.loads(parsed_data)

      if parsed_data is None:
        raise Exception("parsed user query response is not available")

      g.parsed_user_query = parsed_data

      return f(*args, **kwargs)
    except Exception as e:
      return jsonify({
        'success': False,
        'error': str(e)
      }), 400
  return wrapper