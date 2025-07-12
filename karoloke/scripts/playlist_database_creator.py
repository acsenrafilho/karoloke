import json
import os
import pathlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print
from rich.console import Console

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

SCHEMA_PATH = Path(__file__).parent / 'playlist_schema.json'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_PATH = Path(__file__).parent / f'playlist_output_{timestamp}.json'

# # Gemini API call
# def call_gemini_api(pdf_text: str, schema: dict) -> dict:
#     client = genai.Client(api_key=GEMINI_API_KEY)
#     prompt = (
#         "Interpret the following PDF text and organize the data as a JSON structure. Take care to not mix the table rows, because each row represents a single JSON input in the structure. "
#         "Use this JSON schema: " + json.dumps(schema) + "\nPDF text:\n" + pdf_text
#     )
#     console = Console()
#     with console.status("[bold green]Consultando Gemini API...[/]", spinner="dots"):
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt,
#             config={"temperature": 0}
#         )
#     try:
#         result_json = json.loads(response.text)
#     except Exception:
#         result_json = {"error": "Could not parse Gemini response as JSON", "raw": response.text}
#     return result_json


def call_gemini_api_with_pdf(pdf_path: str, schema: dict) -> dict:
    """
    Calls Gemini API with the actual PDF file and schema.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF file.
    schema : dict
        JSON schema for the playlist.

    Returns
    -------
    dict
        Gemini API response as a JSON structure.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = (
        'Interpret the attached PDF file and organize the data as a JSON structure. '
        'Each table row should be a single JSON entry.'
    )

    # Retrieve and encode the PDF byte
    filepath = pathlib.Path(pdf_path)

    console = Console()
    with console.status(
        '[bold green]Consultando Gemini API...[/]', spinner='dots'
    ):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=filepath.read_bytes(),
                    mime_type='application/pdf',
                ),
            ],
            config={
                'temperature': 0,
                'response_mime_type': 'application/json',
                'response_schema': schema,
            },
        )
    try:
        result_json = json.loads(response.text)
    except Exception:
        result_json = {
            'error': 'Could not parse Gemini response as JSON',
            'raw': response.text,
        }
    return result_json


def read_pdf_pages(pdf_path: str, page_range: Tuple[int, int]) -> str:
    doc = fitz.open(pdf_path)
    start, end = page_range
    text = ''
    for page_num in range(start, end + 1):
        page = doc.load_page(page_num - 1)  # PyMuPDF is 0-indexed
        text += page.get_text()
    return text


def main(pdf_path: str, page_range: Tuple[int, int]):
    print('Starting the Playlist Database Creator...')

    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)

    # Call GeminiAPI with PDF file
    print('Calling Gemini API with PDF file...', end='')
    result_json = call_gemini_api_with_pdf(pdf_path, schema)
    print(' done.')

    # Save output
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(result_json, f, indent=2, ensure_ascii=False)
    print(f'Output saved to {OUTPUT_PATH}')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            'Usage: python playlist_database_creator.py <pdf_path> <start_page> <end_page>'
        )
        sys.exit(1)
    pdf_path = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])
    main(pdf_path, (start_page, end_page))
