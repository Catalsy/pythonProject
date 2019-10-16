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
			user_adress text NOT NULL,
			phone_number text NOT NULL)"""
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
        # EXPLAINED
		#	 order_time column: 
 		# 		TIMESTAMP is a type of data, is has a date/time format.
		#	 	DEFAULT: means that if we do not insert anything in that field, by DEFAULT the dabase is going to 
		#	 	put in that field the CURRENT_TIMESTAMP aka current date and time.
		#	 	in other words, everytime the users makes an order, the system is going to store the date/time automatically.
		#	 FOREIGN KEY:
		#		we should keep track of which usered ordered each ordered. So we should have a way of saying 'The user id 
  		# 		in this table is going to be same one as in the users table'.
  		# 		that's why we use FOREIGN KEY, it gives us the ability to relate (or reference) a column from one table 
    	# 		to a column from another table. IT IS NOT A NEW COLUMN CALLED 'FOREIGN KEY' IT IS A PROPERTY OF THE TABLE.
		#		in this case, the column 'user_id' from the 'orders' table, is going to have the same value as the 
		#		column 'user_id' from the table 'users'. 
        
    createTables()
        

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)