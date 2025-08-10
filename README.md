# Job Assistant Toolkit

A small collection of Python tools that help with job hunting by:
- Scraping career pages (with BeautifulSoup) and extracting relevant role listings.
- Comparing a CV to a job description and drafting a concise cover letter via the OpenAI API.
- Recommending job roles and search links based on resume text.

---

## Contents

- `Job Search` – Fetches a careers page and asks an LLM to extract particular roles.
- `CV Coverletter` – Fetches a job description from a URL, reads a CV PDF, validates inputs, and (if valid) asks an LLM to analyze fit and draft a cover letter.
- `Job Recommender` – Reads a resume PDF, asks an LLM to summarize skills, and suggests relevant roles with job‑search links by location and site.
- `requirements.txt` – Dependencies for all scripts.
- `.env` – environment variables to copy into your own `.env` (do **not** commit real keys).


---

## Features

- **OpenAI API** to call GPT models (e.g., `gpt-4o-mini`) for summarization, matching, and drafting cover letters.
- **BeautifulSoup** (`bs4`) and `requests` for fetching and parsing job postings from the web.
- **PDF parsing** via `pypdf` or `PyPDF2` to extract resume text.


---

## Prerequisites

- An OpenAI API key

---

## Setup

1) **Clone the repo**
```bash
git clone https://github.com/Sameeh07/Job-Assistant.git
cd Job-Assistant/folder_name
```

2) **Create a virtual environment (optional but recommended)**
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3) **Install dependencies**
```bash
pip install -r requirements.txt
```

4) **Configure environment variables**  
Create a `.env` file in the project root (same folder as the scripts).


Edit `.env` and add your keys:
```dotenv
# Required for OpenAI API calls
OPENAI_API_KEY=sk-...

# Optional: if you use the Groq endpoint with OpenAI client in job_search_from_notebook.py
# GROQ_API_KEY=...
```

> Keep your real keys out of version control.

---

## Tips & Notes

- **Web scraping**: Some sites block scraping or require different headers. Respect terms of service.
- **PDF extraction quality** varies depending on how the PDF was created. Scanned PDFs without OCR won’t extract cleanly.
- **Model names**: Adjust for your account access. Defaults often use `gpt-4o-mini` but you can change via flags or env vars.
- **API costs**: LLM calls can incur costs. Keep an eye on token usage.

---


## License

Add your preferred license here (e.g., MIT).

