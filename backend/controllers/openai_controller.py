from flask import Blueprint, request, jsonify
from openai import OpenAI
import os


openai_bp = Blueprint("openai", __name__)

client = OpenAI(
  api_key=os.environ.get("OPEN_API_KEY")
)

@openai_bp.post("/chat")
def chat():
  try:

    data = request.get_json()
    user_query = data['prompt']

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": 'You are a coding assistant that talks like a pirate.'
        },
        {
          "role": "user",
          "content": user_query
        }
      ]
    )

    chat_response = response.choices[0].message.content

    return jsonify({"response": chat_response})

  except Exception as e:
    print(e)
