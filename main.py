import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini API key missing in .env file.")
    
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    
    if response.usage_metadata == None:
        raise RuntimeError("API response .usage_metadata is None - api call may have failed.")
    
    if args.verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(f"Response:\n{response.text}")   




if __name__ == "__main__":
    main()
