import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import sys
from functions.call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(
                    prog='AI Chatbot',
                    description='Answers user provided prompts using the Google Gemini AI')

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = 'gemini-2.5-flash'

def main():
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    user_prompt = args.user_prompt
    if args.verbose:
        print(f"User prompt: {user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        if response.usage_metadata is not None:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            if args.verbose:
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")
        else:
            raise RuntimeError("Failed API Request")
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.function_calls:
            function_results_list = []
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if len(function_call_result.parts) == 0:
                    raise Exception("Function call result is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function response is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function response response is None")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results_list.append(function_call_result.parts[0])
        else:
            print(response.text)

if __name__ == "__main__":
    main()
