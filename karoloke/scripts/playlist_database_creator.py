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
from karoloke.scripts.playlist_schema import PlaylistItem

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

SCHEMA_PATH = Path(__file__).parent / 'playlist_schema.json'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_PATH = Path(__file__).parent / f'playlist_output_{timestamp}.json'

def call_gemini_api_with_pdf(pdf_path: str) -> dict:
    """
    Calls Gemini API with the actual PDF file and playlist_schema.
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
                'response_schema': list[PlaylistItem],
            },
        )
    try:
        # Try to extract the text from the Gemini response
        result_text = None
        if hasattr(response, 'candidates') and response.candidates:
            content = getattr(response.candidates[0], 'content', None)
            if content and hasattr(content, 'parts'):
                parts = content.parts
                if parts and hasattr(parts[0], 'text'):
                    result_text = parts[0].text
        if not result_text:
            result_text = getattr(response, 'text', None)
        result_json = json.loads(result_text) if result_text else {'error': 'No response text', 'raw': str(response)}
    except Exception:
        result_json = {'error': 'Could not parse Gemini response as JSON', 'raw': str(response)}
    return result_json


def main(pdf_path: str):
    print('Starting the Playlist Database Creator...')
    # Call GeminiAPI with PDF file and playlist_schema
    print('Calling Gemini API with PDF file...', end='')
    result_json = call_gemini_api_with_pdf(pdf_path)
    print(' done.')

    # Save output
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(result_json, f, indent=2, ensure_ascii=False)
    print(f'Output saved to {OUTPUT_PATH}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Usage: python playlist_database_creator.py <pdf_path>'
        )
        sys.exit(1)
    pdf_path = sys.argv[1]
    main(pdf_path)
