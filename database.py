# Claude code was used to code this
import psycopg2

from email_parser import EmailParser


class ApplicationDB:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=job_applications user=job_tracker")
        self.cur = self.conn.cursor()

    def add_application(self, email):
        company = email["from"]
        company_name = EmailParser.get_company(company)
        print(company_name)

        return email
