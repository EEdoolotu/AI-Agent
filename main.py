import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types








def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error, pls input a command")
        sys.exit(1)

    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
    )
    print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f" Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f" Response tokens: {response.usage_metadata.candidates_token_count}")

    

    









if __name__ == "__main__":
    main()
