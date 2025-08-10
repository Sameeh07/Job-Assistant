
import argparse
import io
import os
import re
import sys
import time
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

# ----------------------------
# Setup
# ----------------------------

load_dotenv(override=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

SYSTEM_PROMPT = """
You are an assistant who analyzes user's CV against the job description 
and provide a short summary if the user is fit for this job. If the user is fit for the job, 
write a cover letter for the user to apply for the job. Keep the cover letter professional, short, 
and formal.

Important things to notice before analyzing CV:
1. Always check if the CV is actually a CV or just random text
2. Check if the job description fetched from the website is the job description or not
   and ignore text related to navigation
3. Also check the link of the job posting, if it actually resembles a job posting or is just a fake website
4. If any one of these two checks fails, do not analyze the CV against the job description and give an
   appropriate response as you think
5. Always respond in Markdown.
"""


# ----------------------------
# Utilities
# ----------------------------

def is_probable_job_url(url: str) -> bool:
    """Heuristic check that URL looks like a real job posting."""
    if not re.match(r"^https?://", url or ""):  # basic scheme check
        return False
    # common path hints
    hints = ["/jobs", "/careers", "/job/", "/positions", "/openings", "/positions/"]
    return any(h in url.lower() for h in hints)


def fetch_job_text(url: str, timeout: int = 25) -> Tuple[str, str]:
    """Return (title, text) from a job posting page."""
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    # Remove clearly irrelevant elements
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer", "header"
                                     , "noscript", "svg", "button", "form"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    return title, text


def extract_pdf_text(path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                # fall back: ignore problematic page
                pass
    return "\n".join(chunks).strip()


def looks_like_cv(text: str) -> bool:
    """Heuristic check for CV-ish content."""
    if not text or len(text) < 500:  # very short unlikely to be a CV
        return False
    cues = ["experience", "education", "skills", "projects", "summary", "work", "certification"]
    count = sum(1 for c in cues if c in text.lower())
    return count >= 2


def looks_like_job_description(text: str) -> bool:
    """Heuristic check for JD-ish content."""
    if not text or len(text) < 500:
        return False
    cues = ["responsibilities", "requirements", "qualifications", "role", "about the role", "what you'll do"]
    count = sum(1 for c in cues if c in text.lower())
    return count >= 1


def build_user_prompt(job_text: str, cv_text: str, url: str) -> str:
    return f"""
Job Posting:
{job_text}

CV:
{cv_text}

Url:
{url}
"""


def main():
    parser = argparse.ArgumentParser(description="Analyze CV vs Job Description and draft a cover letter if it's a fit.")
    parser.add_argument("--job-url", required=True, help="URL of the job posting")
    parser.add_argument("--cv", required=True, help="Path to CV PDF file")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), help="OpenAI model to use (default: gpt-4o-mini)")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[error] OPENAI_API_KEY not set. Put it in a .env or environment.", file=sys.stderr)
        sys.exit(2)

    # Validate inputs quickly
    if not is_probable_job_url(args.job_url):
        print("[notice] The provided URL doesn't look like a typical job posting. The assistant may decline to analyze.")
    if not os.path.exists(args.cv):
        print(f"[error] CV file not found: {args.cv}", file=sys.stderr)
        sys.exit(2)

    # Fetch and parse job description
    try:
        job_title, job_text = fetch_job_text(args.job_url)
    except Exception as e:
        print(f"[error] Failed to fetch job posting: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract CV text
    try:
        cv_text = extract_pdf_text(args.cv)
    except Exception as e:
        print(f"[error] Failed to extract CV: {e}", file=sys.stderr)
        sys.exit(1)

    # Heuristic validation (mirrors notebook logic/intent)
    if not looks_like_job_description(job_text) or not looks_like_cv(cv_text):
        generic = (
            "It looks like either the job posting URL/text or the CV content may be invalid or incomplete.\n\n"
            "Please make sure you: \n"            "- Paste a real job posting URL (from a careers site or job board)\n"            "- Provide a proper CV PDF (not random text or a scan without selectable text)\n\n"
            "Once both are valid, I can analyze the CV against the job description and draft a short cover letter."
        )
        print(generic)
        sys.exit(0)

    # Build prompts
    user_prompt = build_user_prompt(job_text, cv_text, args.job_url)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    # OpenAI client
    client = OpenAI()

    # Call API
    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0.2,
        )
        content = resp.choices[0].message.content
    except Exception as e:
        print(f"[error] OpenAI API error: {e}", file=sys.stderr)
        sys.exit(1)

    # Print markdown response
    print(content)


if __name__ == "__main__":
    main()
