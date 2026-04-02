import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import sys


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(
                    prog='AI Chatbot',
                    description='Answers user provided prompts using the Google Gemini AI')


def main():
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    user_prompt = args.user_prompt
    if args.verbose:
        print(f"User prompt: {user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        if args.verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        raise RuntimeError("Failed API Request")
    print(response.text)
    #print("Hello from ai-chatbot!")

if __name__ == "__main__":
    main()
