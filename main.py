import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini API key missing in .env file.")
    
    client = genai.Client(api_key=api_key)
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model="gemini-2.5-flash", contents=user_prompt)
    
    if response.usage_metadata == None:
        raise RuntimeError("API response .usage_metadata is None - api call may have failed.")
    
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")   




if __name__ == "__main__":
    main()
