import time

import connection
from functions import *
import plotext as plt
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
import os
import sys
from key_generator.key_generator import generate

def main():
    just_fix_windows_console()

    balance = 5000
    stocks_price = 228.14
    inp = 0
    player_stocks = 0
    day = 0
    next_day = True
    inventary = []
    prices = []
    conn = connection.Conn()
    name = ""

    LOGO()

    while True:
        print(f""" Чтобы играть вам нужно {Fore.LIGHTRED_EX}зарегистрироваться{Fore.RESET}/{Fore.LIGHTGREEN_EX}войти{Fore.RESET} в аккаунт
         {Fore.LIGHTRED_EX}Зарегистрироваться{Fore.RESET} 1
         {Fore.LIGHTGREEN_EX}Войти в существующий аккаунт{Fore.RESET} 2""")

        inp = int(input())
        if inp == 1:
            print('---')
            print(
                f' {Fore.LIGHTGREEN_EX}Введите ваш никнейм (может содержать буквы, цифры и специальные символы, максимальная длина 20, аккаунты с непристойными никнеймами будут удалены){Fore.RESET}')
            nick = input()
            print(f' {Fore.LIGHTBLUE_EX}Введите пароль (может содержать буквы, цифры и специальные символы, максимальная длина 20){Fore.RESET}')
            psw = input()
            if conn.register(nick, psw, balance, player_stocks):
                l = conn.login(nick, psw)
                if len(l) == 0:
                    inp = input()
                id = l[0]
                name = l[1]
                print(f' {Fore.LIGHTYELLOW_EX}Успешная регистрация!{Fore.RESET}')
                break
            time.sleep(0.5)

        elif inp == 2:
            print('---')
            print(
                f' {Fore.LIGHTGREEN_EX}Введите ваш никнейм{Fore.RESET}')
            nick = input()
            print(f' {Fore.LIGHTBLUE_EX}Введите пароль{Fore.RESET}')
            psw = input()
            l = conn.login(nick, psw)
            if len(l) == 0:
                inp = input()
            id = l[0]
            name = l[1]
            balance = l[3]
            player_stocks = l[4]
            print(f' {Fore.LIGHTYELLOW_EX}Успешная авторизация!{Fore.RESET}')

            time.sleep(1)
            break

    while True:

        all = conn.get_all(id, balance, player_stocks)

        stocks_price = all[0]

        DRAW_PLOT(all[2])
        # EVERYDAY NEWS
        print(f"--- \n"
              f" Криптовалюта Газпром стоит на данный момент: {Fore.LIGHTBLUE_EX}{round(stocks_price, 2)}{Fore.RESET} \n"
              f"---")

        print(
            f" Ваш баланс: {Fore.GREEN}{round(balance, 2)}{Fore.RESET}\n"
            f" Ваш баланс на криптокошельке: {Fore.BLUE}{round(player_stocks * stocks_price, 2)}{Fore.RESET}\n"
            f" Осталось секунд до обновления курса криптовалюты: {Fore.YELLOW}{all[3]}{Fore.RESET}")

        print(f"""---\n Текущие транзакции:""")
        for transactions in all[4]: print(transactions)

        print(f"""--- {Fore.CYAN}Топ игроков:{Fore.RESET}""")
        for top_players in all[5]: print(top_players)

        print(f"---\n"
              f" {Fore.LIGHTGREEN_EX}Приобрести криптовалюту 1{Fore.RESET}\n"
              f" {Fore.LIGHTRED_EX}Продать криптовалюту 2{Fore.RESET}\n"
              f" {Fore.LIGHTYELLOW_EX}Обновить биржу 3{Fore.RESET}\n"
              f" {Fore.LIGHTBLUE_EX}Магазин 7{Fore.RESET}\n"
              f"---")

        try:
            query = int(input())
        except:
            print("Неверный ввод")
            time.sleep(1)
            continue

        # BUY STOCKS
        if query == 1:
            print(f"--- \n Введите кол-во рублей \n Ваш баланс позволяет купить криптовалюту Газпром на: {balance} рублей\n Чтобы купить криптовалюту на все деньги введите -1 \n---")
            try:
                inp = float(input())
            except:
                print("Неверный ввод")
                time.sleep(1)
                continue

            if inp == -1:
                inp = balance

            if inp < 0:
                print("Неверный ввод")
                time.sleep(1)
                continue

            if inp > balance:
                print("Недостаточно средств")
                time.sleep(0.5)
                continue
            time.sleep(0.5)
            print(f"--- \n Покупка выполняется...")
            time.sleep(0.5)

            # hackers = random.randint(0, 500)
            # hackers = (hackers / 100 / 100) * inp

            # if not "защита от DDOS-атак" in inventary:
            #     print(f" Хакеры взломали биржу и ограбили вас на {hackers} рублей.\n"
            #           f" Купите защиту от DDOS-атак за 1.000.000 в магазине")

            print(f" Поздравляем, вы купили криптовалюту на {inp} рублей по цене {round(stocks_price, 2)}!\n")
            BUY_SOUND()
            inp /= stocks_price
            conn.buy_stocks(name, inp)
            balance -= inp * stocks_price

            komisiya = random.uniform(2, 5) * inp / 100
            print(f" Коммисия банка {komisiya} руб.")
            inp -= komisiya

            choice = random.randint(1, 10)
            if choice == 1:
                moshonka = random.uniform(1, 3) * inp / 100
                print(f" Вас ограбили мошенники на {moshonka} руб.")
                inp -= moshonka

            player_stocks += inp

        # SELL STOCKS
        if query == 2:
            print(f"--- \nВведите кол-во рублей на которые вы хотите продать крипту")
            print(f"Ваш баланс позволяет продать: {round(player_stocks * stocks_price, 2)} рублей\n Чтобы купить криптовалюту на все деньги введите -1\n---")
            try:
                inp = float(input())
            except Exception as e:
                print(f"Неверный ввод, ошибка {e}")
                time.sleep(1)
                continue

            if inp == -1:
                inp = player_stocks * stocks_price

            if inp < 0:
                print("Неверный ввод")
                time.sleep(1)
                continue

            if inp > player_stocks * stocks_price:
                print("Вы не можете продать так много криптовалюты")
                time.sleep(1)
                print()
                continue
            time.sleep(0.5)
            print("--- \n Подготовливаем к продаже...")
            time.sleep(0.5)

            print(" Ищем покупателя...")
            time.sleep(random.triangular(0.5, 4))
            print(f" Поздравляем, вы продали криптовалюту Газпром на {inp} рублей по цене {round(stocks_price, 2)}!")
            SELL_SOUND()
            print()
            inp /= stocks_price
            conn.sell_stocks(name, inp)
            player_stocks -= inp

            komisiya = random.uniform(2, 5) * inp / 100
            print(f" Коммисия банка {komisiya} руб.")
            inp -= komisiya

            choice = random.randint(1, 10)
            if choice == 1:
                moshonka = random.uniform(1, 3) * inp / 100
                print(f" Вас ограбили мошенники на {moshonka} руб.")
                inp -= moshonka

            balance += inp * stocks_price
            next_day = True

        # RELOAD STOCKS
        if query == 3:
            clear = lambda: os.system('cls')
            clear()
            continue

        # SHOP
        if query == 7:
            # print('---\nМагазин DИS\nВременно не работает')
            # time.sleep(0.5)
            # continue
            print('---\nМагазин DИS\nДоступные товары:')

            for item_id, item_info in items.items():
                print(f' {item_id}. {item_info["name"]} - {item_info["price"]} рублей')

            print(' Чтобы выйти из магазина напишите 7\n---')

            while True:
                goods = int(input('Чтобы выбрать товар, напишите его номер: '))

                if goods == 7: break

                if goods not in items:
                    print("Такого продукта нет.")
                    continue

                if balance < items[goods]["price"]:
                    print(f'Недостаточно средств. Требуется {items[goods]["price"]} рублей.')
                    continue

                print(f'---\n Вы приобрели {items[goods]["name"]}!')
                SHOP_SOUND()
                balance -= items[goods]["price"]
                inventary.append(goods)
                items.clear()
                next_day = True

                key = generate(seed=time.time()).get_key()
                conn.register_key(str(key))
                print(f" Ваш ключ к игре: {key}")
                print(" Ключ действует только один раз")
                break

            print(" Нажмите любую клавишу для продолжения")
            a = input()
            time.sleep(0.5)

        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()

try:
    main()
except Exception as e:
    print("Вы получили ошибку", e)
    time.sleep(0.5)
    print("Пожалуйста, скопируйте это сообщение и отошлите @noootle в тг")
    a = input()