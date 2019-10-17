import psycopg2

try:
    # required information to use the db 
    conn = psycopg2.connect(
        database = "pythonproject", # database name
        user = "postgres",
        password = "Nowhere25Man", #your password
        host = "127.0.0.1",
        port = "5432"
    )
    
    def createTables(): # function to create the tables
        cursor = conn.cursor()
        
        # create product table
        cursor.execute(
            """CREATE TABLE products (
			product_id int primary key NOT NULL,
			product_type text NOT NULL,
			product_model text NOT NULL,
			product_price int NOT NULL,
            product_details text)"""
		)
        conn.commit()
        
        # create user information table
        cursor.execute(
			"""CREATE TABLE users (
			user_id SERIAL NOT NULL PRIMARY KEY,
			user_username text NOT NULL,
			user_fullname text NOT NULL,
			user_email text NOT NULL,
			user_password text NOT NULL,
			user_adress text,
			phone_number text)"""
   		) #FULLNAME
        conn.commit()
        
        cursor.execute(
            """CREATE TABLE orders (
            order_number SERIAL NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            order_status text NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id))"""
		) #PENDING #
        conn.commit()
        cursor.close()
                
    createTables()
        

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)