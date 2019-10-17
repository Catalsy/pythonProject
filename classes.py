import psycopg2

try:
    # required information to use the db 
    conn = psycopg2.connect(
        database = "pythonproject", # database name
        user = "postgres",
        password = "6108", #your password
        host = "127.0.0.1",
        port = "5432"
    )
    
    class Users:
        def __init__(self, username = None, name = None, email = None, password = None, adress = None, phone_number = None):
            self.username = username
            self.name = name
            self.email = email
            self.password = password
            self.adress = adress
            self.phone_number = phone_number
            
        def register(self):
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (user_username, user_name, user_email, user_password, user_adress, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)""", (self.username, self.name, self.email, self.password, self.adress, self.phone_number)
            )
            conn.commit()
            cursor.close()


except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)

    