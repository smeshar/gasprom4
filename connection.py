import pymysql
# from mysql.connector import Error
from colorama import Fore, Back, Style
import passwords
import time


class Conn():
    def __init__(self):
        self.hostname = passwords.hostname
        self.database = passwords.database
        self.password = passwords.password
        self.port = passwords.port
        self.username = passwords.username

    def connect(self):
        self.connection = pymysql.connect(host=self.hostname, database=self.database, user=self.username,
                                          password=self.password,
                                          port=self.port)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_prices(self):
        prices = list()
        self.cursor.execute("SELECT * FROM prices")
        rows = self.cursor.fetchall()

        for i in range(max(0, len(rows) - 15), len(rows)):
            prices.append(rows[i][0])

        return prices

    def get_days(self):
        self.cursor.execute("SELECT * FROM prices")
        rows = self.cursor.fetchall()
        return len(rows)

    def login(self, name: str, password: str):
        self.connect()
        query = f"SELECT * FROM users WHERE name = '{name}'"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        self.close()
        if len(rows) == 0:
            print(" Несуществующий пользователь")
            return []

        passw = rows[0][2]
        if passw != password:
            print(" Неверный пароль")
            return []

        return rows[0]

    def register(self, name, password, balance, player_stocks):
        self.connect()
        query = f"SELECT * FROM users WHERE name = '{name}'"
        self.cursor.execute(query)
        if len(self.cursor.fetchall()) != 0:
            print("Пользователь с таким никнеймом уже существует")
            self.close()
            return 0

        query = f"""INSERT INTO users (name, password, balance, player_stocks)
                VALUES ('{name}', '{password}', {balance}, {player_stocks})
                """
        self.cursor.execute(query)
        self.connection.commit()
        self.close()
        return 1

    def get_price(self):
        query = f"SELECT stocks_price FROM config"
        self.cursor.execute(query)

        rows = self.cursor.fetchone()
        if rows is None:
            print("Error update config database")
            return 0
        return rows[0]

    def top_ten(self):
        query = f"SELECT * FROM users ORDER BY balance DESC"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        l = []

        for i in range(min(10, len(rows))):
            l.append(f"{Fore.CYAN}{i + 1}. {rows[i][1]} - {rows[i][3]} руб.{Fore.RESET}")

        return l

    def time_to_reload(self):
        query = "SELECT day FROM config"
        self.cursor.execute(query)

        rows = self.cursor.fetchone()

        return rows[0]

    def buy_stocks(self, name, value):
        self.connect()
        query = f"""insert into queue (name, opt, value) values ('{name}', 1, {value})"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close()

    def sell_stocks(self, name, value):
        self.connect()
        query = f"""insert into queue (name, opt, value) values ('{name}', 0, {value})"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close()

    def update(self, id, balance, player_stocks):
        query = f"UPDATE users SET balance = {balance}, player_stocks = {player_stocks} where id = {id}"
        self.cursor.execute(query)
        self.connection.commit()

    def get_day(self):
        query = f"SELECT day FROM config"
        self.cursor.execute(query)
        rows = self.cursor.fetchone()
        if rows is None:
            return -1
        return rows[0]

    def transactions(self):
        self.cursor.execute("select stocks_price from config")
        rows = self.cursor.fetchone()
        while rows is None:
            self.cursor.execute("select stocks_price from config")
            rows = self.cursor.fetchone()
            time.sleep(0.5)

        stocks_price = rows[0]

        query = f"SELECT * FROM queue"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return [" Пока ничего нет"]

        l = []
        for row in rows:
            x = f"купил" if row[1] == 1 else f"продал"
            l.append(f" {row[0]} {x} крипты на {round(row[2] * stocks_price, 2)}руб.")
        return l

    def get_ping(self):
        curtime = time.time()
        self.connect()
        ans = time.time() - curtime
        self.close()

        ans = round(ans * 1000)

        if ans < 100:
            return Fore.LIGHTGREEN_EX + str(ans) + Fore.RESET
        if ans > 300:
            return Fore.LIGHTRED_EX + str(ans) + Fore.RESET
        return Fore.LIGHTYELLOW_EX + str(ans) + Fore.RESET

    def get_all(self, id, balance, player_stocks) -> list:
        self.connect()

        l = [self.get_price(), self.get_day(), self.get_prices(), self.time_to_reload(), self.transactions(),
             self.top_ten(), self.get_days()]
        self.update(id, balance, player_stocks)

        self.close()
        l.append(self.get_ping())
        return l

    def fetch_all(self) -> list:
        query = "SELECT * FROM config"
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        l = list()

        for row in rows:
            l.append(row)

        return l

    def register_key(self, gamekey):
        self.connect()
        query = f"INSERT INTO gamekeys VALUES ('{gamekey}')"
        self.cursor.execute(query)
        self.close()

    def get_version(self):
        self.connect()
        query = f"select * from version"
        self.cursor.execute(query)
        current_version = self.cursor.fetchall()[-1][0]
        return current_version

# c = Conn()
