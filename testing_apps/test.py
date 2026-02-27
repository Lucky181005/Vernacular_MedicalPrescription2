import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY_TEST")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

# Create client
client = genai.Client(api_key=api_key)

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",   # Safe and recommended
    contents="Explain Artificial Intelligence in 2 simple lines."
)

print("\nResponse:\n")
print(response.text)