import os

# Neo4j settings
URL      = "bolt://localhost:7687"
USER     = os.environ["NEO4J_USER"]
PASSWORD = os.environ["NEO4J_PASSWORD"]

# OpenAI / LLM settings
OPEN_API_KEY = os.environ["OPENAI_API_KEY"]
GOOGLE_GEMINI_KEY = os.environ["GOOGLE_GEMINI_KEY"]