import hashlib, binascii, os, psycopg2, re
#from classes import User

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
        username = input("Username: ").lower()
        name = input("Name: ").title()
        
        while True:
            email = input("Email: ")
            
            if check_email(email):
                break
            else:
                print("Invalid Email\n")
                
        password = hash_password(input("Password: "))
        adress = input("Adress: ")
        
        while True:
            phone_number = input("Phone Number: ")
            
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
    

    
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)


 
