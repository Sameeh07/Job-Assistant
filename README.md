# Job Assistant Toolkit

A small collection of Python tools that help with job hunting by:
- Scraping career pages (with BeautifulSoup) and extracting relevant DevOps/SRE listings.
- Comparing a CV to a job description and drafting a concise cover letter via the OpenAI API.
- Recommending job roles and search links based on resume text.

All tools are runnable locally with a simple `git clone` + `pip install -r requirements.txt` flow.

---

## Contents

- `job_search_from_notebook.py` – Fetches a careers page and asks an LLM to extract DevOps/SRE/Platform/CI-CD roles.
- `cv_job_matcher.py` – CLI that fetches a job description from a URL, reads a CV PDF, validates inputs, and (if valid) asks an LLM to analyze fit and draft a cover letter.
- `resume_job_reco.py` – Reads a resume PDF, asks an LLM to summarize skills, and suggests relevant roles with job‑search links by location and site.
- `requirements.txt` – Dependencies for all scripts.
- `.env.example` – Example environment variables to copy into your own `.env` (do **not** commit real keys).

> Note: Script names are suggestions; feel free to rename your local files accordingly.

---

## Features

- **OpenAI API** to call GPT models (e.g., `gpt-4o-mini`) for summarization, matching, and drafting cover letters.
- **BeautifulSoup** (`bs4`) and `requests` for fetching and parsing job postings from the web.
- **PDF parsing** via `pypdf` or `PyPDF2` to extract resume text.
- Input validation heuristics (e.g., checks that URLs look like job postings and that PDFs resemble real CVs).
- Clean CLI UX (flags like `--job-url`, `--cv`) with clear error messages.

---

## Prerequisites

- Python 3.9+ recommended
- An OpenAI API key

---

## Setup

1) **Clone the repo**
```bash
git clone <your_repo_url>
cd <your_repo_folder>
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
Create a `.env` file in the project root (same folder as the scripts). You can start from `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```dotenv
# Required for OpenAI API calls
OPENAI_API_KEY=sk-...

# Optional: if you use the Groq endpoint with OpenAI client in job_search_from_notebook.py
# GROQ_API_KEY=...
```

> Keep your real keys out of version control.

---

## Usage

### 1) Extract DevOps/SRE roles from a careers page
Script: `job_search_from_notebook.py`

```bash
python job_search_from_notebook.py
```
- Fetches: `https://www.google.com/about/careers/applications/jobs` (default in script).
- Sends the page text to an LLM with instructions to extract **DevOps/SRE/Platform/CI-CD** roles.
- Prints a Markdown list of roles, companies, and (when possible) links.

> Environment: this script is configured to use the OpenAI client with a **Groq** base URL and `GROQ_API_KEY`. You can switch to normal OpenAI usage if preferred.

---

### 2) Compare CV vs Job Description and draft a cover letter
Script: `cv_job_matcher.py`

```bash
python cv_job_matcher.py --job-url https://example.com/job/123 --cv ./YourCV.pdf
```

- Fetches the job posting HTML, removes obvious boilerplate, and extracts text.
- Extracts text from your CV PDF.
- Validates both inputs with simple heuristics:
  - URL looks like a job posting (`/jobs`, `/careers`, `/job/`, etc.)
  - CV and JD are long enough and contain typical section cues.
- If valid, sends both to the OpenAI API to analyze fit and draft a **short, professional** cover letter.
- Prints Markdown output to the console.

Optional:
```bash
# Choose a different model
python cv_job_matcher.py --job-url <url> --cv <path> --model gpt-4o-mini
```

---

### 3) Resume-based role suggestions with search links
Script: `resume_job_reco.py`

Interactive flow:
```bash
python resume_job_reco.py
# enter resume path, job sites (e.g., "LinkedIn Indeed Naukri Glassdoor"), and location
```

What it does:
- Reads your resume PDF text via `pypdf`.
- Crafts a prompt asking the model to summarize the resume and propose job roles.
- Requests search links for each role across the provided job sites and location.

---

## Requirements

See `requirements.txt` (example):
```
beautifulsoup4
python-dotenv
requests
openai
pypdf
PyPDF2
```

> You might not need both `pypdf` and `PyPDF2` if you standardize on one across all scripts. Keep both if you plan to run all scripts as-is.

---

## Tips & Notes

- **Web scraping**: Some sites block scraping or require different headers. Respect robots.txt and terms of service.
- **PDF extraction quality** varies depending on how the PDF was created. Scanned PDFs without OCR won’t extract cleanly.
- **Model names**: Adjust for your account access. Defaults often use `gpt-4o-mini` but you can change via flags or env vars.
- **API costs**: LLM calls can incur costs. Keep an eye on token usage.

---

## Troubleshooting

- *“No API key found”*: Ensure `.env` exists and `OPENAI_API_KEY` is set.
- *Bad resume path*: Check the path exists and is readable.
- *Empty or garbled PDF text*: Your PDF might be scanned or protected. Try exporting to PDF again or apply OCR.
- *403/429 from websites*: Add/retry with different headers, or wait/rate-limit requests.

---

## License

Add your preferred license here (e.g., MIT).

