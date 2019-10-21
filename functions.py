import hashlib
import binascii
import os
import psycopg2
import re
import getpass

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


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
        print(" - USER REGISTRATION - ")

        # username input and check
        while True:
            username = input("\nUsername: ").lower()

            cursor = conn.cursor()
            cursor.execute(
                """SELECT user_username FROM users WHERE user_username = '%s'""" % username)
            records = cursor.fetchall()
            cursor.close()

            if records:
                print("Sorry! That username already exists! Let's try another one")
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
                    print("Sorry! That email is already in use! Let's try another one")

                else:
                    break

            else:
                print(
                    "Invalid Email adress, it should follow the format \"something@something.something\"\n")

        # password hash and verification
        while True:
            password = hash_password(getpass.getpass("\nPassword: "))
            confirm_password = getpass.getpass("Confirm Password: ")

            if verify_password(password, confirm_password):
                break

            else:
                print("Passwords don't match, please try again\n")

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

        current_user_id = record[0][0]
        login = True

        print("Thank you for registering!\n")

    def main_menu():
        # shows main menu and returns product_id of selected product

        clear()
        print("""
               _________________
              |      MENU       |
              |_________________|
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
                    print("Please type a number within the range\n")

                else:
                    break
            except:
                print("Please, only numbers\n")
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
                selected_option = int(
                    input(f"Please select an option to add to the cart [1 - {option_counter}]: "))

                if selected_option < 1 or selected_option > (option_counter):
                    print("Please type a number within the range\n")

                else:
                    break
            except:
                print("Please, only numbers\n")

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

    def summary():

        if login == False:
            while True:
                account = input(
                    "Do you have an account with us? (Y/N): ").upper()

                if account[:1] == 'Y':
                    # log_in()
                    break

                elif account[:1] == 'N':
                    print("")
                    register_user()
                    break

                else:
                    print("Please, type \'Y\' or \'N\'\n")

        print()

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
                if data[0][0] == None:
                    print("For delivery we will need more information: ")

                    # phone number input and check
                    while True:
                        phone_number = input("\nPhone Number: ")

                        if len(str(phone_number)) != 10:
                            print("Please, type a 10 digit phone number\n")

                        else:
                            try:
                                phone_number = int(phone_number)
                                break

                            except:
                                print(
                                    "Invalid phone number, please only type numbers\n")

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
                    break

            elif pickup_or_delivery[:1] == "P":
                print("You chose pickup")
                print()
                break

            else:
                print("Please, type \'P\' or \'D\'\n")

        cursor = conn.cursor()
        cursor.execute("""SELECT orders.order_number,
                        CONCAT(INITCAP(TO_CHAR(orders.order_time, 'day')),', ',
                        INITCAP(TO_CHAR(orders.order_time, 'mon')), ' ',
                        INITCAP(TO_CHAR(orders.order_time, 'dd'))),
                        products.product_model,
                        CONCAT(products.product_price)
                        FROM orders INNER JOIN products
                        ON orders.product_id = products.product_id
                        WHERE user_id = '%s' AND order_status = 'cart'""" % current_user_id)
        orders = cursor.fetchall()
        cursor.close()

        total = 0
        prices = []
        if orders:
            print("""
               _________________
              |     SUMMARY     |
              |_________________|
              """)

            for order in orders:
                print(f"""Order #{order[0]}
                Product: {order[2]}
                Date: {order[1]}
                Price: ${order[3]}""")
                prices.append(int(order[3]))

                subtotal = 0

                for x in prices:
                    subtotal = subtotal + x

                tax = subtotal * 0.07
                total = subtotal + tax

                print()

                print("Subtotal -- ${:.2f}".format(subtotal))
                print("Taxes ----- ${:.2f}".format(tax))
                print("Total ----- ${:.2f}".format(total))

        else:
            print("Your cart is empty")

        return(total)

    def checkout():
        print("We only accept ")


except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)