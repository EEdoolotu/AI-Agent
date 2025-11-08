import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function  # expects to return a types.Content with function_response part
from config import MAX_ITERS


def main():
    verbose = "--verbose" in sys.argv

    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set")
        sys.exit(1)
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

    user_prompt = sys.argv[1]

    # Build the Tool from your function schemas
    tools = [
        types.Tool(function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ])
    ]

    # Start the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(MAX_ITERS):
        if verbose:
            print(f"\n--- iteration {i+1}/{MAX_ITERS} ---")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction=system_prompt,
            ),
        )

        # If the model produced plain text with no tool calls, we're done.
        if not getattr(response, "function_calls", None):
            if verbose:
                print("No function calls. Final text:")
            print(response.text or "")
            return

        # Optionally see what the model tried to call
        if verbose:
            for fc in response.function_calls:
                print(f"Function call -> name={fc.name}, args={fc.args}")

        # Execute each function call and collect their function_response parts
        function_responses_parts = []
        for fc in response.function_calls:
            fr_content = call_function(fc, verbose=verbose)
            # Expect call_function to return a types.Content with parts[0].function_response
            if (
                not fr_content.parts
                or not fr_content.parts[0].function_response
            ):
                raise RuntimeError("empty function call result")
            if verbose:
                print(f"-> {fr_content.parts[0].function_response.response}")
            function_responses_parts.append(fr_content.parts[0])

        # Add the model’s function call *request* back (optional but helps some models chain)
        if response.candidates and response.candidates[0].content:
            messages.append(response.candidates[0].content)

        # Add the function responses back to the conversation so the model can use them
        messages.append(types.Content(role="user", parts=function_responses_parts))

    # If we exit the loop, we hit the iteration cap.
    print(f"Maximum iterations ({MAX_ITERS}) reached.")
    sys.exit(1)


if __name__ == "__main__":
    main()
