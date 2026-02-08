import os
from email.message import EmailMessage

from dotenv import load_dotenv

from client import EmailClient
from database import ApplicationDB
from email_parser import EmailParser

_ = load_dotenv()

address = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
server = os.getenv("SERVER")


def main():
    try:
        if address and password and server:
            db = ApplicationDB()
            client = EmailClient(address, password, server)
            client.connect()
            ids = client.get_email_ids()
            for id in ids:
                raw = client.get_email_content(id)

                if not isinstance(raw, EmailMessage):
                    raise RuntimeError("error getting email")

                parser = EmailParser()
                email = parser.parse_email(raw)

                if parser.is_application(email):
                    # if parser.is_rejection(email):
                    # print("Rejection " + email["from"])
                    # else:
                    # print("Application " + email["from"])
                    db.add_application(email)

        else:
            print("Env error")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
