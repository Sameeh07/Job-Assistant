import os
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url: str):
        self.url = url
        try:
            
            response = requests.get(self.url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            self.text = soup.get_text(separator=" ").lower()
        except Exception as e:
            self.title = "Error"
            self.text = f""
            print(f"[Website] Failed to fetch {self.url}: {e}")

def main():
    job_search = Website("https://www.google.com/about/careers/applications/jobs")
    system_prompt = (
        "You are a job search assistant who finds real-time DevOps-related job listings from "
        "career pages, job boards, and developer platforms. Return results with job title, "
        "company name, and a link to the listing. Focus on DevOps, SRE, Platform Engineering, "
        "and CI/CD tooling roles."
    )

    user_prompt = f"""
Here is a list of job postings:

{job_search.text}

Please extract only the jobs that are clearly related to:
- DevOps
- Site Reliability Engineering (SRE)
- Platform Engineering
- CI/CD or Infrastructure

Exclude roles like sales, instructors, analysts, and anything not related to DevOps tools.

For each DevOps-related job, return:
- Job Title
- Company
- Location
- Years of Experience
- Skill set required
- (if available) Whether it's remote
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=messages,
        temperature=0.2,
    )

    content = response.choices[0].message.content
    print(content)

if __name__ == "__main__":
    main()
