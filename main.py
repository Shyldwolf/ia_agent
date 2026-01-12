import os
import argparse
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_input", type=str, help="The input prompt for content generation.")
    args = parser.parse_args()
    prompt = args.user_input

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )
    
    if not response.usage_metadata:
        raise ValueError("No usage metadata found in the response.")
    
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("response:")
    print(response.text)




if __name__ == "__main__":
    main()
