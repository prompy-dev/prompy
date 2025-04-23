import os

class Config:
  OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
  PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

class DevelopmentConfig(Config):
  ENV = os.environ.get("FLASK_ENV", "development")
  DEBUG = os.environ.get("FLASK_DEBUG")

class TestingConfig(Config):
  pass

class ProductionConfig(Config):
  pass

