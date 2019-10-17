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
    
    def insertProducts(): # function to insert products
        cursor = conn.cursor()
        
        # insert products into database
        cursor.execute(
            """INSERT INTO products (product_id, product_type, product_model, product_price)
            VALUES (001, 'iPhone', 'iPhone 11', 699 ),
                (002, 'iPhone', 'iPhone 11 Pro', 999), 
                (003, 'MacBook', 'MacBook Air 13-inch', 1099),
                (004, 'MacBook', 'MacBook Pro 13-inch', 1299),
                (005, 'iPad', 'iPad', 329),
                (006, 'iPad', 'iPad Pro 11-inch ', 799),
                (007, 'Apple Watch', 'Apple Watch Series 5', 399),
                (008, 'AirPods', 'AirPods w/ Wireless Charging Case', 199)"""
		) 
        # not adding product details yet
        conn.commit()
        cursor.close()
        
    insertProducts()
        

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data PostgreSQL", error)