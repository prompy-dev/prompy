import os
from openai import OpenAI

class OpenAIClientException(Exception):
  """
  Custom exception for handling errors related to OpenAI API interactions.
  
  Attributes:
    message (str): Description of the error.
  """
  def __init__(self, message):
    self.message = message

  def __str__(self):
    return f'OpenAIClientException: {self.message}'


class OpenAIChatClient:
  """
  Client for interacting with the OpenAI Chat Completion API using a conversational model.

  Attributes:
    model (str): The name of the model to use (e.g., "gpt-4").
    config (dict): Additional configuration options to pass to the API call.
    client (OpenAI): An initialized OpenAI client.
    messages (list): The history of messages used in the chat session.
  """

  def __init__(self, model, config):
    """
    Initializes the chat client with the given model and config.

    Args:
      model (str): The model to be used for completions.
      config (dict): Additional API parameters (e.g., temperature, max_tokens).
    """
    self.model = model
    self.config = config
    self.client = OpenAI(api_key=os.environ.get("OPEN_API_KEY"))
    self.messages = []

  def create(self, user_prompt):
    """
    Sends a prompt to the OpenAI chat model and returns the assistant's response.

    Args:
      user_prompt (str): The user's input message.

    Returns:
      str: The model-generated assistant response.

    Raises:
      OpenAIClientException: If the API call fails or no response is returned.
    """
    try:
      self.messages.append(self.create_message(role='user', content=user_prompt))

      api_response = self.client.chat.completions.create(
          model=self.model,
          messages=self.messages,
          **self.config
      )

      chat_response = api_response.choices[0].message.content

      if not chat_response:
        raise OpenAIClientException(message="OpenAI API did not return a result")

    except:
      raise OpenAIClientException(message="Failed to connect to OpenAI API")

    else:
      # Log the response (can be redirected to a logger)
      print('LOGGING RESULT ====', chat_response)

      self.messages.append(self.create_message(role='assistant', content=chat_response))
      return chat_response

  def create_message(self, role: str, content: str):
    """
    Constructs a message dictionary in the format expected by the OpenAI API.

    Args:
      role (str): The role of the message sender ('system', 'user', or 'assistant').
      content (str): The message content.

    Returns:
      dict: A message dictionary.
    """
    return { "role": role, "content": content }

  def set_system_prompt(self, prompt: str):
    """
    Adds a system-level instruction to guide the behavior of the assistant.

    Args:
      prompt (str): The instruction text for the system role.
    """
    self.messages.append(self.create_message(role='system', content=prompt))


class OpenAIEmbeddingClient:
  """
  Client for creating embeddings using OpenAI's embedding models.

  Attributes:
    model (str): The embedding model to use (e.g., "text-embedding-ada-002").
    client (OpenAI): An initialized OpenAI client.
  """

  def __init__(self, model):
    """
    Initializes the embedding client with the given model.

    Args:
      model (str): The model used to create embeddings.
    """
    self.client = OpenAI(api_key=os.environ.get("OPEN_API_KEY"))
    self.model = model

  def create(self, input: str):
    """
    Generates an embedding for the given input text.

    Args:
      input (str): The text to be embedded.

    Returns:
      list[float]: A list of floats representing the embedding.

    Raises:
      OpenAIClientException: If the API call fails or returns no embedding.
    """
    try:
      response = self.client.embeddings.create(
        input=input,
        model=self.model,
        encoding_format="float"
      )

      embedding = response.data[0].embedding

      if not embedding:
        raise OpenAIClientException(message="Failed to connect to OpenAI API")

    except:
      raise OpenAIClientException(message="Failed to create embedding")

    else:
      # Log the result (can be redirected to a logger)
      print('LOGGING RESULT ====', embedding)

      return embedding
