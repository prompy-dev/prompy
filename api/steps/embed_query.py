import os
from langchain_openai import OpenAIEmbeddings


embedder = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=os.environ.get("OPEN_API_KEY")
)
