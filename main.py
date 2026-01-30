import os

from dotenv import load_dotenv

from client import EmailClient

load_dotenv()

email = os.getenv("ADDRESS")
password = os.getenv("PASSWORD")
server = os.getenv("SERVER")

if __name__ == "__main__":
    client = EmailClient(email, password, server)
    client.Connect()
