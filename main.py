import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import available_functions



def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("Error, pls input a command")
        sys.exit(1)

    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]


    
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt,
        ),
    )
    calls = response.function_calls
    for item in calls:
        print(type(calls[0]))
        print(dir(calls[0]))


    print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f" Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f" Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    

    









if __name__ == "__main__":
    main()
