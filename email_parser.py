from email.message import EmailMessage

from bs4 import BeautifulSoup


class EmailParser:
    @staticmethod
    def parseEmail(email: EmailMessage):
        subject = email["subject"]
        from_ = email["from"]
        print(from_)
        body = ""

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
        }
