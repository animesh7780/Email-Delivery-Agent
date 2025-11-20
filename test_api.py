"""
Quick test script to verify Gemini API key
"""
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    print("Please add your Gemini API key to the .env file.")
    exit(1)

print(f"Testing API Key: {api_key[:20]}...")
print(f"Testing Model: {model_name}")
print("-" * 50)

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    print("Sending test request...")
    response = model.generate_content("Say 'API is working!' if you receive this.")
    
    print("\n✅ SUCCESS!")
    print("Response:", response.text)
    print("\nYour Gemini API key is working correctly! 🎉")
    
except Exception as e:
    print("\n❌ ERROR!")
    print(f"Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. Invalid model name")
    print("3. API quota exceeded")
    print("4. Network connection issue")
