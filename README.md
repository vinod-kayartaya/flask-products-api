# Flask Products API

A RESTful API for managing products built with Flask and SQLite3.

## Prerequisites

- Python 3.11 or higher
- Docker (optional)

## Environment Variables

The application can be configured using the following environment variables:

- `DB_PATH`: SQLite database file path (default: `products.db`)

## Database Setup

You can initialize the database using the provided `db_init.sql` script or via Flask CLI:

```bash
# Using SQLite command line
sqlite3 products.db < db_init.sql

# Or using Flask CLI
flask init-db

# Or using Python
python -c "from app import init_db; init_db()"
```

The script will:

1. Create the `products` table with the following columns:
   - id (auto-incrementing primary key)
   - name (TEXT)
   - price (REAL)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)
2. Create an automatic trigger to update the `updated_at` timestamp when rows are modified
3. Create an index on the `name` column for faster searches
4. Insert 10 sample products

## Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set environment variables:

```bash
export DB_PATH=products.db
```

3. Initialize the database:

```bash
flask init-db
```

4. Run the application:

```bash
# Using gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or using Python directly (automatically initializes DB if missing)
python app.py
```

## Docker Setup

1. Build the Docker image:

```bash
docker build -t flask-products-api .
```

2. Run the container:

```bash
docker run -p 8000:8000 flask-products-api
```

To persist the database across container restarts, mount a volume:

```bash
docker run -p 8000:8000 -v $(pwd)/products.db:/app/products.db flask-products-api
```

## API Endpoints

- `GET /api/products` - Get all products
- `POST /api/products` - Create a new product
- `GET /api/products/{product_id}` - Get a specific product
- `PUT /api/products/{product_id}` - Update a product
- `DELETE /api/products/{product_id}` - Delete a product

## Example Requests

### Create a product

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Product 1", "price": 99.99}'
```

### Get all products

```bash
curl http://localhost:8000/api/products
```

### Get a specific product

```bash
curl http://localhost:8000/api/products/1
```

### Update a product

```bash
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Product", "price": 149.99}'
```

### Delete a product

```bash
curl -X DELETE http://localhost:8000/api/products/1
```
