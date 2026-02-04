import os
from email.message import EmailMessage

from dotenv import load_dotenv

from client import EmailClient
from email_parser import EmailParser

_ = load_dotenv()

email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
server = os.getenv("SERVER")

if __name__ == "__main__":
    try:
        if email and password and server:
            client = EmailClient(email, password, server)
            client.Connect()
            ids = client.GetEmailsId()
            for id in ids:
                raw = client.GetEmailContent(id)

                if raw is not EmailMessage:
                    raise RuntimeError("error getting email")
                email = EmailParser.parseEmail(raw)

        else:
            print("Env error")

    except Exception as e:
        print(e)
