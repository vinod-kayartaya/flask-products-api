# Flask Products API

A RESTful API for managing products built with Flask and MySQL.

## Prerequisites

- Python 3.11 or higher
- MySQL Server
- Docker (optional)

## Environment Variables

The application can be configured using the following environment variables:

- `DB_HOST`: MySQL host (default: localhost)
- `DB_PORT`: MySQL port (default: 3306)
- `DB_USER`: MySQL user (default: root)
- `DB_PASSWORD`: MySQL password (default: root)
- `DB_NAME`: MySQL database name (default: products)

## Database Setup

You can initialize the database using the provided `db_init.sql` script:

```bash
# Using MySQL command line
mysql -u root -p < db_init.sql

# Or using Docker if you have MySQL running in a container
docker exec -i mysql-container mysql -u root -p < db_init.sql
```

The script will:

1. Create the database if it doesn't exist
2. Create the products table with the following columns:
   - id (auto-incrementing primary key)
   - name (VARCHAR)
   - price (DECIMAL)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)
3. Insert 10 sample products
4. Create an index on the name column for faster searches

## Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=root
export DB_NAME=products
```

3. Run the application:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Docker Setup

1. Build the Docker image:

```bash
docker build -t flask-products-api .
```

2. Run the container with environment variables:

```bash
docker run -p 8000:8000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=3306 \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  -e DB_NAME=products \
  flask-products-api
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
