from flask import Flask, request, jsonify, g
import sqlite3
import os
import time
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database configuration from environment variable with fallback value
DB_PATH = os.getenv('DB_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.db'))

@app.before_request
def log_request_info():
    g.start_time = time.time()
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    query_params = f"?{request.query_string.decode('utf-8')}" if request.query_string else ""
    logger.info(f"Incoming Request: {request.method} {request.path}{query_params} from {client_ip}")

@app.after_request
def log_response_info(response):
    start_time = getattr(g, 'start_time', None)
    duration = f"{(time.time() - start_time) * 1000:.2f}ms" if start_time else "N/A"
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logger.info(
        f"Completed Request: {request.method} {request.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration} | "
        f"Client: {client_ip}"
    )
    return response

def get_db_connection():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        logger.error(f"Error connecting to SQLite: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_init.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            logger.info("Database initialized successfully.")
        conn.close()

@app.cli.command('init-db')
def init_db_command():
    """Initialize the database with schema and sample data."""
    init_db()
    print('Initialized the database.')

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to fetch products: Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = [dict(row) for row in cursor.fetchall()]
        logger.info(f"Fetched {len(products)} products")
        return jsonify(products)
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching products: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        logger.warning("Failed to create product: 'name' and 'price' are required")
        return jsonify({'error': 'Name and price are required'}), 400
    
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to create product: Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO products (name, price) VALUES (?, ?)"
        cursor.execute(query, (data['name'], data['price']))
        conn.commit()
        product_id = cursor.lastrowid
        logger.info(f"Created product with ID {product_id}: '{data['name']}' (${data['price']})")
        return jsonify({'id': product_id, 'name': data['name'], 'price': data['price']}), 201
    except sqlite3.Error as e:
        logger.error(f"Database error while creating product: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    if not conn:
        logger.error(f"Failed to fetch product {product_id}: Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            logger.info(f"Retrieved product {product_id}")
            return jsonify(dict(row))
        logger.warning(f"Product {product_id} not found")
        return jsonify({'error': 'Product not found'}), 404
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching product {product_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        logger.warning(f"Failed to update product {product_id}: 'name' and 'price' are required")
        return jsonify({'error': 'Name and price are required'}), 400
    
    conn = get_db_connection()
    if not conn:
        logger.error(f"Failed to update product {product_id}: Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        query = "UPDATE products SET name = ?, price = ? WHERE id = ?"
        cursor.execute(query, (data['name'], data['price'], product_id))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Product {product_id} not found for update")
            return jsonify({'error': 'Product not found'}), 404
        logger.info(f"Updated product {product_id}: '{data['name']}' (${data['price']})")
        return jsonify({'id': product_id, 'name': data['name'], 'price': data['price']})
    except sqlite3.Error as e:
        logger.error(f"Database error while updating product {product_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    if not conn:
        logger.error(f"Failed to delete product {product_id}: Database connection failed")
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Product {product_id} not found for deletion")
            return jsonify({'error': 'Product not found'}), 404
        logger.info(f"Deleted product {product_id}")
        return '', 204
    except sqlite3.Error as e:
        logger.error(f"Database error while deleting product {product_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host='0.0.0.0', port=8000)
