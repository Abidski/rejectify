import os

from dotenv import load_dotenv

from client import EmailClient

_ = load_dotenv()

email = os.getenv("ADDRESS")
password = os.getenv("PASSWORD")
server = os.getenv("SERVER")

if __name__ == "__main__":
    try:
        if email and password and server:
            client = EmailClient(email, password, server)
            client.Connect()
            client.GetEmails()
        else:
            print("Env error")

    except Exception as e:
        print(e)
