import imaplib


class EmailClient:
    def __init__(self, address: str, password: str, server: str):
        self.address: str = address
        self.password: str = password
        self.server: str = server
        self.port: int = 993

    def Connect(self):
        client = imaplib.IMAP4_SSL(self.server, self.port)
        connection = client.login(self.address, self.password)
        if connection[0] == "OK":
            print("CONNECTION SUCCESSFUL")
        else:
            print("ERROR CONNECTING TO EMAIL")
