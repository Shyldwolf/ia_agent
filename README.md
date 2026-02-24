# IA Agent (Python CLI + Gemini)

Python CLI agent that generates content using **Google GenAI (Gemini)** and supports a tool/function-calling pattern.

## Features
- CLI usage via `argparse`
- Loads env vars via `python-dotenv`
- Uses `google-genai`
- Iterative loop with tool calls

## Setup
1. Create `.env` with:
   - `GEMINI_API_KEY=your_key_here`

2. Install deps (based on pyproject):
   - `google-genai`
   - `python-dotenv`

## Run
python main.py "Write me a short ad for my services" --verbose
