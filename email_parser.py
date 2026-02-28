import json
import os
import time
from email.message import EmailMessage

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq, RateLimitError


class EmailParser:
    load_dotenv()

    def __init__(self):
        # From claude code
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

    def is_application(self, email):
        response = self.prompt_llm(
            (
                "You are a job application classifier. Your task is to determine if an email is "
                "related to a specific job application process (e.g., confirmations, interviews, "
                "rejections, offers, or recruiter follow-ups).\n\n"
                "Exclusions: Ignore newsletters, job board digests (Indeed/LinkedIn alerts), "
                "and generic marketing. Respond ONLY with a JSON object: "
                "{'is_application': true} or {'is_application': false}."
            ),
            (f"{email['subject']}\n{email['from']}\n{email['body']}"),
        )
        return response

    def get_info(self, email):
        response = self.prompt_llm(
            (
                "You are a specialized assistant that extracts job application details from emails. "
                "Extract these fields: 'company_name', 'position_title', 'is_rejection' (boolean), "
                "and 'status' (one of: applied, rejected, interview, offer, unknown). "
                "If a field is missing, return null. Do NOT guess. Return ONLY a JSON object."
            ),
            (f"{email['from']}\n{email['subject']}\n{email['body'][:2000]}"),
        )
        return response

    def prompt_llm(self, system, user):
        for attempt in range(5):  # Retry up to 5 times
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": system,
                        },
                        {
                            "role": "user",
                            "content": user,
                        },
                    ],
                    temperature=0,
                    max_completion_tokens=512,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )

                return json.loads(completion.choices[0].message.content)
            except RateLimitError as e:
                print(e)
                # Extract wait time from error if possible, or use a default
                wait_time = 2**attempt  # Exponential: 1, 2, 4, 8s
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
        raise Exception("Failed after multiple retries due to rate limits.")
