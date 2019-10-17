import hashlib, binascii, os, psycopg2, re, getpass

#GLOBAL VARIABLES
user_id = 0
login = False

def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                provided_password.encode('utf-8'), 
                                salt.encode('ascii'),
                                100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def check_email(email):
    #checks for valid email
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' 
    if(re.search(regex,email)):   
        return True
    
    else:    
        return False

try:
    # required information to use the db 
    conn = psycopg2.connect(
        database = "pythonproject", # database name
        user = "postgres",
        password = "Nowhere25Man", #your password
        host = "127.0.0.1",
        port = "5432"
    )
    
    def register_user():
        #Register user into database
        print(" - USER REGISTRATION - ")
        
        #username input and check
        while True:
            username = input("\nUsername: ").lower()
            
            cursor = conn.cursor()
            cursor.execute("""SELECT user_username FROM users WHERE user_username = '%s'""" %username)
            records = cursor.fetchall()
            cursor.close()
            
            if records:
                print("Sorry! That username already exists! Let's try another one")
            else:
                break
        
        name = input("\nName: ").title()
        
        #email input and check
        while True:
            email = input("\nEmail: ")
            
            if check_email(email):
                cursor = conn.cursor()
                cursor.execute("""SELECT user_email FROM users WHERE user_email = '%s'""" %email)
                records = cursor.fetchall()
                cursor.close()
            
                if records:
                    print("Sorry! That email is already in use! Let's try another one")
                    
                else:
                    break
                    
            else:
                print("Invalid Email adress, it should follow the format \"something@something.something\"\n")
        
        #password hash and verification
        while True:
            password = hash_password(getpass.getpass("\nPassword: "))
            confirm_password = getpass.getpass("Confirm Password: ")
            
            if verify_password(password, confirm_password):
                break
            
            else:
                print("Passwords don't match, please try again\n")
        
        adress = input("\nHome adress: ")
        
        #phone number input and check
        while True:
            phone_number = input("\nPhone Number: ")
            
            if len(str(phone_number)) != 10:
                print("Please, type a 10 digit phone number\n")
            
            else:
                try:
                    phone_number = int(phone_number)
                    break
                
                except:
                    print("Invalid phone number, please only type numbers\n")

        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users (user_username, user_fullname, user_email, user_password, user_adress, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)""", (username, name, email, password, adress, phone_number)
        )
        conn.commit()
        cursor.close()
        
        login = True
        print("Thank you for registering!")
        
    
    def main_menu():
        #shows main menu and returns product_id of selected product 
        
        clear()
        print("""
               _________________
              |      MENU       |
              |_________________|
              """)
        print("PRODUCTS & SERVICES:")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT product_type FROM products")
        types = cursor.fetchall()
        cursor.close()
        
        # prints types of services and products
        option_counter = 1
        for product in types:
            print(f"{option_counter}.{product[0]}  ", end='')
            if (option_counter%5) == 0:
                print("") 
            option_counter += 1
        
        # asks to select an option and checks for input
        option_counter -= 1
        print("\n")
        while True:
            try:
                selected_option = int(input(f"Please select an option [1 - {option_counter}]: "))
                
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
            print(f"{option_counter}.{product[0]} ${product[1]}  ", end='')
            if (option_counter%4) == 0:
                print("") 
            option_counter += 1
        
        option_counter -= 1
        print("\n")
        while True:
            try:
                selected_option = int(input(f"Please select an option to add to the cart [1 - {option_counter}]: "))
                
                if selected_option < 1 or selected_option > (option_counter):
                    print("Please type a number within the range\n")
                
                else:
                    break
            except:
                print("Please, only numbers\n")
                
        product_id = models[selected_option - 1][2]
        
        return(product_id)
        
    
    def add_to_cart(product_id):
        # adds selected product to cart (orders table)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO orders (user_id, product_id, order_status)
                       VALUES (%s, %s, 'cart')""", (user_id, product_id))
        conn.commit()
        cursor.close()
    
    

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)