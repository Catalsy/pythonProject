CREATE TABLE products (
    product_id int primary key NOT NULL,
    product_type text NOT NULL,
    product_model text NOT NULL,
    product_price int NOT NULL,
    product_details text
);

CREATE TABLE users (
    user_id SERIAL NOT NULL PRIMARY KEY,
    user_username text NOT NULL,
    user_fullname text NOT NULL,
    user_email text NOT NULL,
    user_password text NOT NULL,
    user_adress text,
    phone_number text
);

CREATE TABLE orders (
    order_number SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status text NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);