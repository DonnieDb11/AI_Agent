import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    
    parser = argparse.ArgumentParser(description="Personal AI Agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="Give a prompt to the AI agent")
    args = parser.parse_args()
    messages = [types.Content(role="user", 
    parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
    
        if response.function_calls is None or len(response.function_calls) == 0:
            print(f"Final Response: {response.text}")
            break

        function_call_result = call_function(response.function_calls[0])
        if not function_call_result.parts:
            raise Exception("Expected function response parts, but got None.")
        
        if function_call_result.parts[0].function_response is None:
            raise Exception("Expected function response, but got None.")
        
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Expected function response content, but got None.")
        
        function_results = []
        function_results.append(function_call_result.parts[0])
        
        if args.verbose:
            
            if response.usage_metadata is None:
                raise RuntimeError("Usage metadata is not available in the response.")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))
    else:
        print("No final response from model.")
        sys.exit(1)
   
    
if __name__ == "__main__":
    main()
