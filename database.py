# Claude code was used to code this

import psycopg2


class ApplicationDB:
    def __init__(self, dbname, user, password, host, port):
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cur = self.conn.cursor()
        except Exception:
            print("Error connecting to database")
            raise

    def disconnect(self):
        """From claude"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("✓ Disconnected")

    def add_company(self, info):
        company = info.get("company_name")
        if company is None:
            raise RuntimeError("Error extractiing company")

        try:
            self.cur.execute("SELECT id FROM company WHERE name = %s", (company,))
            result = self.cur.fetchone()

            if result is None:
                self.cur.execute("INSERT INTO company(name) VALUES (%s)", (company,))
                self.conn.commit()

        except Exception as e:
            print("Error adding company", e)
            self.conn.rollback()
            return None

    def get_application(self, company, position):
        try:
            self.cur.execute(
                """
                SELECT a.id,company_id,position_title FROM applications a
                JOIN company c ON c.id = a.company_id
                WHERE c.name = %s AND a.position_title = %s

                """,
                (company, position),
            )
            result = self.cur.fetchone()
            return result
        except Exception as e:
            print("Error getting application", e)
            return None

    def change_application_status(
        self, application_id, company_id, position_title, new_status, date
    ):
        try:
            self.cur.execute(
                """
                UPDATE applications
                SET application_status = %s, update_date = %s
                WHERE id = %s AND company_id = %s AND position_title = %s;
                """,
                (new_status, date, application_id, company_id, position_title),
            )
            self.conn.commit()

            return True

        except Exception:
            self.conn.rollback()
            raise RuntimeError("Error changing the applications status")

    def add_application(self, info, email):
        self.add_company(info)

        company = info.get("company_name")
        position = info.get("position_title")
        rejection = info.get("is_rejection")
        status = info.get("status")
        date = email["date"]
        try:
            if rejection is True or status != "applied":
                print(company)
                print(position)
                info = self.get_application(company, position)
                if info is None:
                    raise RuntimeError("unble to get application info")
                application_id = info[0]
                company_id = info[1]
                position_title = info[2]
                self.change_application_status(
                    application_id, company_id, position_title, status, date
                )

            elif status == "applied":
                self.cur.execute(
                    """
                    INSERT INTO applications (company_id, position_title, application_date, application_status)
                    SELECT 
                        (SELECT id FROM company WHERE name = %s),
                        %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM applications
                        INNER JOIN company ON applications.company_id = company.id
                        WHERE position_title = %s AND company.name = %s
                    )
                    RETURNING id
                    """,
                    (company, position, date, status, position, company),
                )
                self.conn.commit()
                result = (
                    self.cur.fetchone()
                )  # None if it already existed, has id if inserted
        except Exception as e:
            raise RuntimeError("Error changing the applications status", e)
