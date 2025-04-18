from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from config import OPEN_API_KEY, GOOGLE_GEMINI_KEY

openai_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000,
    timeout=None,
    max_retries=2,
    openai_api_key=OPEN_API_KEY
)

google_gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",google_api_key=GOOGLE_GEMINI_KEY)