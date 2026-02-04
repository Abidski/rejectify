import imaplib
from email.parser import Parser
from email.policy import default


class EmailClient:
    def __init__(self, address: str, password: str, server: str):
        self.address: str = address
        self.password: str = password
        self.server: str = server
        self.port: int = 993
        self.client: imaplib.IMAP4_SSL | None = None

    def Connect(self):
        self.client = imaplib.IMAP4_SSL(self.server, self.port)
        connection = self.client.login(self.address, self.password)
        if connection[0] != "OK":
            print("ERROR CONNECTING TO EMAIL")

    def GetEmailsId(self):
        if self.client is None:
            raise RuntimeError("Cannot establish client")

        _ = self.client.select("INBOX", readonly=True)

        _, mail = self.client.search(None, "ALL")
        mailId = mail[0].split()

        return mailId

    def GetEmailContent(self, id):
        if self.client is None:
            raise RuntimeError("Email client not established")
        try:
            _, content = self.client.fetch(id, "(RFC822)")

            if content is None:
                raise RuntimeError("Cannot establish client")

            if content[0] is None:
                raise RuntimeError("Cannot establish client")

            if content[0][1] is None:
                raise RuntimeError("Cannot establish client")

            if isinstance(content, tuple):
                raise RuntimeError("Cannot establish client")

            if not isinstance(content[0][1], bytes):
                raise RuntimeError("Cannot establish client")

            stringContent = content[0][1].decode("utf-8")
            headers = Parser(policy=default).parsestr(stringContent)

            return headers

        except Exception as e:
            print(e)
