from google import genai
from core.config import settings

# Initialize the GenAI client
ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
