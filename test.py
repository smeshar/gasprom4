import pymysql
from mysql.connector import Error
import passwords


class Conn():
    def __init__(self):
        hostname = passwords.hostname
        database = passwords.database
        password = passwords.password
        port = passwords.port
        username = passwords.username

        self.connection = pymysql.connect(host=hostname, database=database, user=username, password=password,
                                          port=port)
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()
            self.cursor.execute("select database();")
            record = self.cursor.fetchone()
            print("You're connected to database: ", record)
            self.connection.commit()

    def func(self):
        query = """SELECT * FROM config"""
        self.cursor.execute(query)
        print(self.cursor.fetchall())
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


c = Conn()
c.func()
c.close()
