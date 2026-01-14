import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from prompts import system_prompt
from functions.call_function import available_functions, call_function

MAX_ITERATIONS = 20

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    parser = argparse.ArgumentParser(description="Generate content using Gemini API.")
    parser.add_argument("user_input", type=str, help="The input prompt for content generation.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_input)])]

    client = genai.Client(api_key=api_key)

    for iteration in range(MAX_ITERATIONS):
        try:
            # Llamada al modelo
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    temperature=0
                ),
            )

            # Guardamos los resultados de funciones de esta iteración
            function_results = []

            # Primero, agregamos las respuestas candidatas del modelo a la historia
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)

            # Revisamos si el modelo quiere llamar a alguna función
            if response.function_calls:
                for function_call in response.function_calls:
                    result = call_function(function_call, verbose=args.verbose)

                    if not result.parts or result.parts[0].function_response is None:
                        raise ValueError("Function call returned invalid result.")

                    response_data = result.parts[0].function_response.response
                    function_results.append(result.parts[0])

                    # Siempre imprimir el resultado
                    print(response_data)

                    # Info extra si verbose
                    if args.verbose:
                        print(f"-> Function '{function_call.name}' executed with args: {function_call.args}")

                # Agregamos los resultados de las funciones a la historia
                if function_results:
                    messages.append(types.Content(role="user", parts=function_results))

            else:
                # No hay más llamadas a funciones: el modelo terminó
                if response.text:
                    print(response.text)
                return  # Salimos del loop

        except ClientError as e:
            if e.code == 429:
                print("Prompt tokens: 0")
                print("Response tokens: 0")
                print("response:")
                print("Error: Rate limit exceeded. Please try again later.")
                return
            else:
                raise

    # Si llegamos al máximo de iteraciones sin obtener respuesta final
    print(f"Error: Max iterations ({MAX_ITERATIONS}) reached without final response.")
    exit(1)


if __name__ == "__main__":
    main()
