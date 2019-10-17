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
    
    def dropTables(): # function to drop the tables
        cursor = conn.cursor()
        
        cursor.execute(
            """DROP TABLE orders"""
		)
        conn.commit()
        cursor.execute(
            """DROP TABLE products"""
		)
        conn.commit()
        cursor.execute(
            """DROP TABLE users"""
		)
        conn.commit()
        
        cursor.close()
    dropTables()
        

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)