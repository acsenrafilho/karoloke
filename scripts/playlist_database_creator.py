import json
import os
import sys
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd
import tabula
from rich import print
from rich.console import Console

# Output paths
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_DIR = Path(__file__).parent
FINAL_OUTPUT = OUTPUT_DIR / f'playlist_output_{timestamp}.json'
STATIC_OUTPUT = (
    Path(__file__).parents[1] / 'karoloke' / 'static' / 'playlist.json'
)

# Column mapping heuristics
COLUMN_ALIASES = {
    'filename': [
        'filename',
        'code',
        'number',
        'id',
        'número',
        'musica',
        'música',
    ],
    'artist': ['artist', 'cantor', 'artista', 'banda'],
    'title': ['title', 'song', 'título', 'musica', 'música'],
    'part': ['part', 'versão', 'observação', 'obs', 'nota'],
}


def pick_column(columns, targets):
    cols_lower = [c.strip().lower() for c in columns]
    for t in targets:
        if t in cols_lower:
            return cols_lower.index(t)
    return None


def sanitize_filename(val: str) -> str:
    if val is None:
        return ''
    s = str(val).strip()
    # Keep digits/letters only, common in karaoke numbers; remove spaces
    s = ''.join(ch for ch in s if ch.isalnum())
    return s


def extract_page_tables(pdf_path: str, page: int) -> list[dict]:
    try:
        dfs = tabula.read_pdf(
            pdf_path, pages=page, multiple_tables=True, lattice=True
        )
    except Exception:
        dfs = tabula.read_pdf(
            pdf_path, pages=page, multiple_tables=True, stream=True
        )

    items: list[dict] = []
    for df in dfs or []:
        if not isinstance(df, pd.DataFrame) or df.empty:
            continue
        df = df.dropna(how='all')
        df.columns = [str(c).strip().lower() for c in df.columns]
        col_map_idx = {}
        for key, aliases in COLUMN_ALIASES.items():
            idx = pick_column(df.columns, aliases)
            if idx is not None:
                col_map_idx[key] = df.columns[idx]
        if 'filename' not in col_map_idx or 'title' not in col_map_idx:
            continue
        artist_col = col_map_idx.get('artist')
        part_col = col_map_idx.get('part')
        for _, r in df.iterrows():
            row_dict = r.to_dict()
            item = {
                'filename': sanitize_filename(
                    row_dict.get(col_map_idx['filename'], '')
                ),
                'artist': str(row_dict.get(artist_col, '') or '').strip()
                if artist_col
                else '',
                'title': str(
                    row_dict.get(col_map_idx['title'], '') or ''
                ).strip(),
                'part': str(row_dict.get(part_col, '') or '').strip()
                if part_col
                else '',
            }
            if not item['filename'] or not item['title']:
                continue
            items.append(item)
    return items


def save_json(data: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main(pdf_path: str):
    print('[bold]Starting Tabula-based playlist extraction[/]')
    # Count pages for progress output
    try:
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        doc.close()
    except Exception:
        total_pages = None

    items: list[dict] = []
    if total_pages:
        for page in range(1, total_pages + 1):
            print(f'[cyan]Page {page}/{total_pages}[/]')
            page_items = extract_page_tables(pdf_path, page)
            items.extend(page_items)
    else:
        print('[yellow]Could not determine page count; reading all pages[/]')
        items = extract_page_tables(pdf_path, 'all')

    print(f'[green]Extracted[/] {len(items)} items from PDF tables')
    save_json(items, FINAL_OUTPUT)
    print(f'[green]Saved timestamped output to[/] {FINAL_OUTPUT}')
    save_json(items, STATIC_OUTPUT)
    print(f'[green]Updated app playlist at[/] {STATIC_OUTPUT}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python playlist_database_creator.py <pdf_path>')
        sys.exit(1)
    pdf_path = sys.argv[1]
    main(pdf_path)
