import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


MAX_ITERS = 20


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Gemini API key missing in .env file.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    # Conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(MAX_ITERS):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("API response .usage_metadata is None - api call may have failed.")

        if args.verbose:
            print(f"[iter {i+1}] Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"[iter {i+1}] Response tokens: {response.usage_metadata.candidates_token_count}")

        # 1) Add ALL candidates' content to the conversation
        if not response.candidates:
            raise RuntimeError("No candidates returned from model")

        for cand in response.candidates:
            if cand.content is not None:
                messages.append(cand.content)

        # 2) If no function calls, we're done
        if not response.function_calls:
            print(f"Final response:\n{response.text}")
            return

        # 3) Execute function calls and collect their Part results
        function_responses = []

        for fc in response.function_calls:
            tool_content = call_function(fc, verbose=args.verbose)

            if not tool_content.parts:
                raise RuntimeError("Tool result had no parts")

            fr = tool_content.parts[0].function_response
            if fr is None:
                raise RuntimeError("Tool result part had no function_response")

            if fr.response is None:
                raise RuntimeError("FunctionResponse.response was None")

            # store the Part for later (as required)
            function_responses.append(tool_content.parts[0])

            if args.verbose:
                print(f"-> {fr.response}")

        # 4) Append tool results back into the conversation as a "user" message
        messages.append(types.Content(role="user", parts=function_responses))

    # If we get here, we hit iteration limit without a final response
    print(f"Error: Reached maximum iterations ({MAX_ITERS}) without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
