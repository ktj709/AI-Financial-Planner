
"""
Responsible for loading PDFs, URLs and simple mock CSVs into a unified document format.
(keeps strictly to the assignment's requirement for ingestion of data sources)
"""
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import os

def load_pdf(file_path: str) -> dict:
    """Extract text from a PDF file and return a dict with source & content."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return {"source": file_path, "content": text}

def fetch_plain_text_url(url: str) -> dict:
    """Fetch plain text from a URL (educational / public resource)."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # minimal: return visible text
    text = "\n".join([p.get_text() for p in soup.find_all("p")])
    return {"source": url, "content": text}

def load_csv_transactions(csv_path: str) -> dict:
    """Load a CSV of transactions; returns path and raw content (caller will parse)."""
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"source": csv_path, "content": content}
