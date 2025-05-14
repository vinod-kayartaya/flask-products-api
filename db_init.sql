-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS products;

-- Use the database
USE products;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO
    products (name, price)
VALUES ('Laptop Pro', 1299.99),
    ('Wireless Mouse', 29.99),
    ('Mechanical Keyboard', 149.99),
    ('4K Monitor', 499.99),
    ('USB-C Hub', 39.99),
    (
        'Noise Cancelling Headphones',
        199.99
    ),
    ('External SSD 1TB', 129.99),
    ('Webcam HD', 79.99),
    ('Gaming Mouse Pad', 24.99),
    ('Bluetooth Speaker', 89.99);

-- Create an index on the name column for faster searches
CREATE INDEX idx_products_name ON products (name);