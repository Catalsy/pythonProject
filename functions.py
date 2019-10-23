import hashlib
import binascii
import os
import psycopg2
import re
import getpass
import time

# GLOBAL VARIABLES
current_user_id = 0
login = False


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))


def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))


def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))


def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))


def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))


def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def validate_card(number):
    numlist = [int(x) for x in reversed(str(number)) if x.isdigit()]
    count = sum(x for i, x in enumerate(numlist) if i % 2 == 0)
    count += sum(sum(divmod(2 * x, 10))
                 for i, x in enumerate(numlist) if i % 2 != 0)
    return (count % 10 == 0)


def hash_password(password):
    # Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    # Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def check_email(email):
    # checks for valid email
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)):
        return True

    else:
        return False


try:
    # required information to use the db
    conn = psycopg2.connect(
        database="pythonproject",  # database name
        user="postgres",
        password="6108",  # your password
        host="127.0.0.1",
        port="5432"
    )

    def register_user():
        # Register user into database
        prCyan(" - USER REGISTRATION - ")

        # username input and check
        while True:
            username = input("\nUsername: ").lower()

            cursor = conn.cursor()
            cursor.execute(
                """SELECT user_username FROM users WHERE user_username = '%s'""" % username)
            records = cursor.fetchall()
            cursor.close()

            if records:
                prRed("USERNAME TAKEN")
            else:
                break

        name = input("\nFull Name: ").title()

        # email input and check
        while True:
            email = input("\nEmail: ")

            if check_email(email):
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT user_email FROM users WHERE user_email = '%s'""" % email)
                records = cursor.fetchall()
                cursor.close()

                if records:
                    prRed("EMAIL ALREADY IN USE")

                else:
                    break

            else:
                prRed(
                    "INVALID EMAIL ADDRESS\n")

        # password hash and verification
        while True:
            password = hash_password(getpass.getpass("\nPassword: "))
            confirm_password = getpass.getpass("Confirm Password: ")

            if verify_password(password, confirm_password):
                break

            else:
                prRed("PASSWORDS DO NOT MATCH\n")

        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (user_username, user_fullname, user_email, user_password)
            VALUES (%s, %s, %s, %s)""", (username, name, email, password)
        )
        conn.commit()
        cursor.close()

        cursor = conn.cursor()
        cursor.execute(
            """SELECT user_id FROM users WHERE user_username = '%s'""" % username
        )
        record = cursor.fetchall()
        cursor.close()
        global current_user_id
        global login
        current_user_id = int(record[0][0])
        login = True

        prYellow("YOU ARE REGISTERED\n")
        time.sleep(1)

    def login_user():
        prCyan("- USER LOGIN -")
        print()

        while True:
            username = input("Username: ").lower()
            password = getpass.getpass("Password: ")
            print()

            cursor = conn.cursor()
            cursor.execute(
                """SELECT user_username, user_password, user_id FROM users WHERE user_username = '%s'""" % username)
            validation = cursor.fetchone()
            cursor.close()

            if validation:
                rigth_pass = verify_password(validation[1], password)
                if rigth_pass:
                    global login
                    login = True
                    global current_user_id
                    current_user_id = int(validation[2])
                    prYellow("YOU ARE LOGGED IN!\n")
                    break
                else:
                    prRed("THE PASSWORD DOESN'T MATCH\n")
            else:
                create_account = input(
                    "Aye young fella, there isn't an account with that username, do you want to register? (Y/N): ").upper()
                print()

                if create_account[:1] == 'Y':
                    register_user()
                    break

                elif create_account[:1] == 'N':
                    print("Okay, try again\n")

                else:
                    prRed("INVALID OPTION\n")
        time.sleep(1)

    def main_menu():
        # shows main menu and returns product_id of selected product

        clear()
        prCyan("""
             /$$      /$$ /$$$$$$$$ /$$   /$$ /$$   /$$      
            | $$$    /$$$| $$_____/| $$$ | $$| $$  | $$      
            | $$$$  /$$$$| $$      | $$$$| $$| $$  | $$      
            | $$ $$/$$ $$| $$$$$   | $$ $$ $$| $$  | $$      
            | $$  $$$| $$| $$__/   | $$  $$$$| $$  | $$      
            | $$\  $ | $$| $$      | $$\  $$$| $$  | $$      
            | $$ \/  | $$| $$$$$$$$| $$ \  $$|  $$$$$$/      
            |__/     |__/|________/|__/  \__/ \______/   
              """)
        print("PRODUCTS & SERVICES:\n")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT product_type FROM products")
        types = cursor.fetchall()
        cursor.close()

        # prints types of services and products
        option_counter = 1
        for product in types:
            print(f"{option_counter}.{product[0]}  ", end='')
            if (option_counter % 5) == 0:
                print("")
            option_counter += 1

        # asks to select an option and checks for input
        option_counter -= 1
        print("\n")
        while True:
            try:
                selected_option = int(
                    input(f"Please select an option [1 - {option_counter}]: "))

                if selected_option < 1 or selected_option > (option_counter):
                    prRed("INVALID OPTION\n")

                else:
                    break
            except:
                prRed("ONLY NUMBERS\n")
        print("")

        selected_option = types[selected_option - 1][0]
        print(f"For {selected_option} we have the next options:\n")

        cursor = conn.cursor()
        cursor.execute(f"""SELECT DISTINCT product_model, product_price, product_id FROM products 
                       WHERE product_type = '{selected_option}' ORDER BY product_model DESC""")
        models = cursor.fetchall()
        cursor.close()

        option_counter = 1
        for product in models:
            print(f"{option_counter}.{product[0]} ${product[1]}  ")

            option_counter += 1

        option_counter -= 1
        print()
        while True:
            try:
                print(
                    f"Please select an option to add to the cart [1 - {option_counter}]")
                selected_option = int(
                    input(f"You can also type '0' to go back to main menu: "))
                print()

                if selected_option == 0:
                    main_menu()
                    break

                elif selected_option < 0 or selected_option > (option_counter):
                    prRed("INVALID OPTION\n")

                else:
                    break
            except:
                prRed("ONLY NUMBERS\n")

        product_id = models[selected_option - 1][2]

        add_to_cart(product_id)

        return(product_id)

    def add_to_cart(product_id):
        # adds selected product to cart (orders table)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO orders (user_id, product_id, order_status)
                       VALUES (%s, %s, 'cart')""", (current_user_id, product_id))
        conn.commit()
        cursor.close()

    def summary(redo=False):
        if login is False:
            while True:
                account = input(
                    "Do you have an account with us? (Y/N): ").upper()

                if account[:1] == 'Y':
                    login_user()
                    break

                elif account[:1] == 'N':
                    print("")
                    register_user()
                    break

                else:
                    prRed("INVALID OPTION\n")

        print()

        if not redo:
            while True:
                pickup_or_delivery = input(
                    "Are you picking up the products or do you want delivery? (P/D): ").upper()

                print()

                if pickup_or_delivery[:1] == "D":

                    cursor = conn.cursor()
                    cursor.execute(f"""SELECT user_adress, phone_number FROM users 
                                WHERE user_id = '{current_user_id}'""")
                    data = cursor.fetchall()
                    cursor.close()

                    # if we don't have the needed data for delivery
                    if data[0][0] is None:
                        print("For delivery we will need more information: ")

                        # phone number input and check
                        while True:
                            phone_number = input("\nPhone Number: ")

                            if len(str(phone_number)) != 10:
                                prRed("INVALID PHONE NUMBER\n")

                            else:
                                try:
                                    phone_number = int(phone_number)
                                    break

                                except:
                                    prRed(
                                        "ONLY NUMBERS\n")

                        adress = input("\nHome adress: ")

                        cursor = conn.cursor()
                        cursor.execute(
                            """UPDATE users SET phone_number = '%s', user_adress = %s
                            WHERE user_id = '%s'""", (phone_number, adress, current_user_id)
                        )
                        conn.commit()
                        cursor.close()
                        break

                    # if we already have it
                    else:
                        print("You chose delivery!\n")
                        time.sleep(1)
                        break

                elif pickup_or_delivery[:1] == "P":
                    print("You chose pickup")
                    time.sleep(1)
                    break

                else:
                    prRed("INVALID OPTION\n")

        cursor = conn.cursor()
        cursor.execute("""SELECT orders.order_number,
                        CONCAT(INITCAP(TO_CHAR(orders.order_time, 'day')),
                        INITCAP(TO_CHAR(orders.order_time, 'mon')), ' ',
                        INITCAP(TO_CHAR(orders.order_time, 'dd'))),
                        products.product_model,
                        CONCAT(products.product_price)
                        FROM orders INNER JOIN products
                        ON orders.product_id = products.product_id
                        WHERE user_id = '%s' AND order_status = 'cart'""" % current_user_id)
        orders = cursor.fetchall()
        cursor.close()

        subtotal = 0
        total = 0
        prices = []
        order_number_collection = []
        if orders:
            clear()
            prCyan("""
              /$$$$$$  /$$   /$$ /$$      /$$ /$$      /$$  /$$$$$$  /$$$$$$$  /$$     /$$
             /$$__  $$| $$  | $$| $$$    /$$$| $$$    /$$$ /$$__  $$| $$__  $$|  $$   /$$/
            | $$  \__/| $$  | $$| $$$$  /$$$$| $$$$  /$$$$| $$  \ $$| $$  \ $$ \  $$ /$$/ 
            |  $$$$$$ | $$  | $$| $$ $$/$$ $$| $$ $$/$$ $$| $$$$$$$$| $$$$$$$/  \  $$$$/  
             \____  $$| $$  | $$| $$  $$$| $$| $$  $$$| $$| $$__  $$| $$__  $$   \  $$/   
             /$$  \ $$| $$  | $$| $$\  $ | $$| $$\  $ | $$| $$  | $$| $$  \ $$    | $$    
            |  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$ \/  | $$| $$  | $$| $$  | $$    | $$    
             \______/  \______/ |__/     |__/|__/     |__/|__/  |__/|__/  |__/    |__/  
              """)

            for order in orders:
                prCyan(f"""Order #{order[0]}
                Product: {order[2]}
                Date: {order[1]}
                Price: ${order[3]}""")
                prices.append(int(order[3]))
                order_number_collection.append(int(order[0]))

                print()

            for x in prices:
                subtotal = subtotal + x

            tax = subtotal * 0.07
            total = subtotal + tax

            prYellow("Subtotal -- ${:.2f}".format(subtotal))
            prYellow("Taxes ----- ${:.2f}".format(tax))
            prYellow("Total ----- ${:.2f}".format(total))
            print()

        else:
            prYellow("YOUR CART IS EMPTY\n")

        while True:
            agree = input("Are you okay with your order? (Y/N): ").upper()
            print()

            if agree[:1] == 'N':
                while True:
                    add_or_remove = input(
                        "Do you want to add or remove products? (A/R): ").upper()
                    print()

                    if add_or_remove[:1] == 'A':
                        print("We are taking you back to the main menu\n")
                        time.sleep(1)
                        main_menu()
                        summary(True)
                        break

                    elif add_or_remove[:1] == 'R':
                        while True:
                            try:
                                order_number = int(
                                    input("Give me the order # of the Item: "))
                                print()

                            except:
                                prRed("ONLY NUMBERS\n")

                            if order_number not in order_number_collection:
                                prRed(
                                    "UNEXISTENT ORDER NUMBER\n")

                            else:
                                break

                        cursor = conn.cursor()
                        cursor.execute(
                            """DELETE FROM orders WHERE order_number = %s""" % order_number)
                        conn.commit()
                        cursor.close()

                        print(f"Order #{order_number} was removed")
                        time.sleep(1)
                        print()
                        summary(True)
                        break

                    else:
                        print("INVALID OPTION\n")

                break

            elif agree[:1] == 'Y':
                print("Awesome, let's proceed with the payment\n")
                break

            else:
                prRed("INVALID OPTION\n")

        return(total)

    def checkout(total):
        if total == 0:
            print(" Thank you for coming! ")
            return 0

        else:
            time.sleep(1)
            clear()
            prGreen("""
             /$$$$$$$   /$$$$$$  /$$     /$$ /$$      /$$ /$$$$$$$$ /$$   /$$ /$$$$$$$$
            | $$__  $$ /$$__  $$|  $$   /$$/| $$$    /$$$| $$_____/| $$$ | $$|__  $$__/
            | $$  \ $$| $$  \ $$ \  $$ /$$/ | $$$$  /$$$$| $$      | $$$$| $$   | $$   
            | $$$$$$$/| $$$$$$$$  \  $$$$/  | $$ $$/$$ $$| $$$$$   | $$ $$ $$   | $$   
            | $$____/ | $$__  $$   \  $$/   | $$  $$$| $$| $$__/   | $$  $$$$   | $$   
            | $$      | $$  | $$    | $$    | $$\  $ | $$| $$      | $$\  $$$   | $$   
            | $$      | $$  | $$    | $$    | $$ \/  | $$| $$$$$$$$| $$ \  $$   | $$   
            |__/      |__/  |__/    |__/    |__/     |__/|________/|__/  \__/   |__/   
            """)

            prCyan("We only accept debit/credit cards:\n")

            while True:
                try:
                    while True:
                        number = int(input("Card number: "))
                        valid = validate_card(number)

                        if not valid:
                            prRed("INVALID CARD NUMBER\n")

                        else:
                            print()
                            break

                    while True:
                        expiration_month = int(
                            input("Expiration month (number): "))

                        if expiration_month > 12 or expiration_month < 1:
                            prRed("INVALID EXPIRATION MONTH\n")

                        else:
                            print()
                            break

                    while True:
                        expiration_year = int(
                            input("Expiration year (full number): "))

                        if expiration_year > 2040 or expiration_year < 2019:
                            prRed("INVALID YEAR NUMBER\n")

                        else:
                            print()
                            break

                    while True:
                        cvv = int(input("CVV: "))

                        if not len(str(cvv)) == 3:
                            prRed("INVALID CVV\n")

                        else:
                            print()
                            break

                    break

                except:
                    prRed("ONLY NUMBERS\n")

            cursor = conn.cursor()
            cursor.execute(
                f"""UPDATE orders SET order_status = 'sold'
                WHERE user_id = {current_user_id} AND order_status = 'cart'"""
            )
            conn.commit()
            cursor.close()

            prYellow(
                "You have been charged ${:.2f}, you're rich LOL".format(total))
            print()
            print("Thank you for your purchase")

    def logout():
        global login
        global current_user_id
        login = False
        current_user_id = 0

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)
