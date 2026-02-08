import re
from email.message import EmailMessage

from bs4 import BeautifulSoup


class EmailParser:
    def __init__(self):
        # Keywords from claude code
        self.keywords = {
            "application": [
                r"application",
                r"applying",
                r"apply",
            ],
            "rejection": [
                r"regret",
                r"unfortunately",
            ],
        }

    def parse_email(self, email: EmailMessage):
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
        for word in self.keywords["application"]:
            if re.search(word, email["subject"].lower()):
                return True

        return False

    def is_rejection(self, email):
        for word in self.keywords["rejection"]:
            if re.search(word, email["body"][:1000].lower()):
                return True

        return False

    @staticmethod
    def get_company_name_from_email(from_):
        index = from_.find(".")
        company_name = from_[0:index].strip()
        return company_name.lower()

    @staticmethod
    def get_company(from_):
        index = from_.find("<")
        company_name = from_[0:index].strip()
        if "@" in company_name:
            get_company_from_email(from_)
        return company_name.lower()
