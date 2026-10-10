-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a trigger to automatically update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_products_timestamp 
AFTER UPDATE OF name, price ON products
FOR EACH ROW
BEGIN
    UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Create an index on the name column for faster searches
CREATE INDEX IF NOT EXISTS idx_products_name ON products (name);

-- Insert sample data
INSERT INTO products (id, name, price) VALUES 
    (1, 'Laptop Pro', 1299.99),
    (2, 'Wireless Mouse', 29.99),
    (3, 'Mechanical Keyboard', 149.99),
    (4, '4K Monitor', 499.99),
    (5, 'USB-C Hub', 39.99),
    (6, 'Noise Cancelling Headphones', 199.99),
    (7, 'External SSD 1TB', 129.99),
    (8, 'Webcam HD', 79.99),
    (9, 'Gaming Mouse Pad', 24.99),
    (10, 'Bluetooth Speaker', 89.99)
ON CONFLICT (id) DO NOTHING;