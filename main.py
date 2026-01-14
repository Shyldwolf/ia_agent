import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_input", type=str, help="The input prompt for content generation.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages =[types.Content(role="user", parts=[types.Part(text=args.user_input)])]

    
    client = genai.Client(api_key=api_key)
    
    try:
        
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
        )
        
    except ClientError as e:
        if e.code == 429:
            print("Prompt tokens: 0")
            print("Response tokens: 0")
            print("response:")
            print("Error: Rate limit exceeded. Please try again later.")
            return
        else:
            raise
    
    
    if not response.usage_metadata:
        raise ValueError("No usage metadata found in the response.")
    
   
    if args.verbose:
        print(f"User prompt: {args.user_input}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

    print(response.text)




if __name__ == "__main__":
    main()
