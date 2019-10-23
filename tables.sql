DROP TABLE orders;

DROP TABLE products;

DROP TABLE users;

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

INSERT INTO
    products (
        product_id,
        product_type,
        product_model,
        product_price
    )
VALUES
    (009, 'iPad', 'iPad', 429),
    (022, 'Music', 'HomePod', 299),
    (010, 'iPad', 'iPad Air', 649),
    (020, 'TV', 'Apple TV HD', 149),
    (021, 'TV', 'Apple TV 4K', 199),
    (017, 'iMac', 'iMac Pro', 4999),
    (001, 'iPhone', 'iPhone 11', 749),
    (002, 'iPhone', 'iPhone XR', 649),
    (018, 'iMac', 'iMac 27inch', 1799),
    (019, 'iMac', 'iMac 21.5inch', 1099),
    (024, 'Music', 'Powerbeats Pro', 249),
    (003, 'iPhone', 'iPhone 8 Plus', 599),
    (004, 'iPhone', 'iPhone 11 Pro', 1149),
    (011, 'iPad', 'iPad Pro 11-inch ', 949),
    (005, 'iPhone', 'iPhone 11 Pro Max', 1249),
    (015, 'Music', 'AirPods Charging Case', 159),
    (006, 'MacBook', 'MacBook Air 13-inch', 1099),
    (007, 'MacBook', 'MacBook Pro 13-inch', 1299),
    (008, 'MacBook', 'MacBook Pro 15-inch', 2399),
    (023, 'Music', 'Beats Solo Pro Wireless', 299),
    (014, 'Apple Watch', 'Apple Watch Edition', 799),
    (013, 'Apple Watch', 'Apple Watch Hermes', 1399),
    (012, 'Apple Watch', 'Apple Watch Series 5', 399),
    (016, 'Music', 'AirPods w/ Wireless Charging Case', 199)
    ;