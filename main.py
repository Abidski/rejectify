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

dbname = os.getenv("DBNAME")
dbuser = os.getenv("DBUSER")
dbpassword = os.getenv("DBPASSWORD")
dbhost = os.getenv("DBHOST")
dbport = os.getenv("DBPORT")


def main():
    try:
        if address and password and server:
            db = ApplicationDB(dbname, dbuser, dbpassword, dbhost, dbport)
            client = EmailClient(address, password, server)
            client.connect()
            ids = client.get_email_ids()
            for id in ids:
                raw = client.get_email_content(id)

                if not isinstance(raw, EmailMessage):
                    print(raw)
                    print(type(raw))
                    raise RuntimeError("error getting email")

                parser = EmailParser()
                email = parser.parse_email(raw)

                info = parser.get_info(email)
                if info.get("is_application"):
                    db.add_application(info, email)

        else:
            print("Env error")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
