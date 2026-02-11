import re
from email.message import EmailMessage

from bs4 import BeautifulSoup


class EmailParser:
    keywords = {
        "application": [
            r"application",
            r"applying",
            r"apply",
        ],
        "rejection": [
            r"regret",
            r"unfortunately",
        ],
        "company": [
            r"is",
            r"at",
            r"with",
        ],
    }

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

    @staticmethod
    def is_application(email):
        for word in EmailParser.keywords["application"]:
            if re.search(word, email["subject"].lower()):
                return True

        return False

    @staticmethod
    def is_rejection(email):
        for word in EmailParser.keywords["rejection"]:
            if re.search(word, email["body"][:1000].lower()):
                return True

        return False

    @staticmethod
    def get_company_name_from_email(email, from_, fullFrom):
        text = email["body"]
        if "greenhouse" in from_:
            match = re.search(r"\bin\s+", text, re.IGNORECASE)
            # Help from claude code
            if not match:
                raise Exception("Error finding company in email body")
            text_after = text[match.end() :]

            capital_match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text_after)
            if not capital_match:
                raise Exception("Error finding company in email body")
            name = capital_match.group(1)
        else:
            at = from_.find("@")
            dot = from_.find(".")
            if dot == -1:
                return from_
            if "workday" in from_:
                name = from_[:at]
            else:
                name = from_[at + 1 : dot]
        return name

    @staticmethod
    def get_company(email, from_):
        index = from_.find("<")
        if index != -1:
            company_name = from_[0:index].strip().strip('"')
        else:
            company_name = from_.strip().strip('"')
        if "@" in company_name:
            clean_name = EmailParser.get_company_name_from_email(
                email, company_name, from_
            )
        else:
            clean_name = re.sub(
                r"notifications?:?", "", company_name, flags=re.IGNORECASE
            ).strip()

        return clean_name.lower()
