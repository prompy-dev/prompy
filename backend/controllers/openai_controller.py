from flask import Blueprint, request, jsonify
from openai import OpenAI
import os


openai_bp = Blueprint("openai", __name__)

client = OpenAI(
  api_key=os.environ.get("OPEN_API_KEY")
)

@openai_bp.route("/chat", methods=["GET"])
def chat():
  try:
    response = client.responses.create(
      model="gpt-4o",
      instructions="You are a coding assistant that talks like a pirate.",
      input="How do I check if a Python object is an instance of a class?",
    )

    return jsonify({"response": response.output_text})
  
  except Exception as e:
    print(e)
