import json
import os
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


class EmailParser:
    load_dotenv()

    def __init__(self):
        self.url = os.getenv("OLLAMA_URL")
        self.model = os.getenv("MODEL")

    @staticmethod
    def parse_email(email: EmailMessage):
        subject = email["subject"]
        from_ = email["from"]
        body = ""

        date = email["Date"]
        # Taken from claude
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_content()

                if part.get_content_type() == "text/html":
                    soup = BeautifulSoup(part.get_content(), "lxml")
                    text = soup.getText(" ", strip=True)
                    body += text
        else:
            if email.get_content_type() == "text/plain":
                body += email.get_content()

            if email.get_content_type() == "text/html":
                soup = BeautifulSoup(email.get_content(), "lxml")
                text = soup.getText(" ", strip=True)
                body += text

        return {
            "subject": subject,
            "from": from_,
            "body": body,
            "date": date,
        }

    def get_info(self, email):
        prompt = f"""Give me the company name of this job application. Respond with ONLY valid JSON.

            From: {email["from"]}
            Subject: {email["subject"]}
            Body: {email["body"][:800]}

            JSON format:
            {{
                "is_application": true/false,
                "is_rejection": true/false,
                "position_title": "title or null",
                "company_name": "actual company name or null",
                "status": "applied|rejected|interview|offer|unknown"
            }}"""

        response = requests.post(
            f"{self.url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.1, "num_predict": 300},
            },
            timeout=120,
        )
        # print(prompt)

        if response.status_code != 200:
            raise Exception("Error from request to llm")

        raw_data = response.json()["response"]

        return json.loads(raw_data)
