
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras
import os
from datetime import datetime
import json
import requests

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
jwt = JWTManager(app)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'finflow_finance'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Verify user with auth service
def verify_user(user_id):
    try:
        auth_service_url = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001')
        response = requests.get(f'{auth_service_url}/api/auth/profile', 
                               headers={'Authorization': f'Bearer {request.headers.get("Authorization", "").replace("Bearer ", "")}'})
        return response.status_code == 200
    except:
        return False

# Initialize database
def init_db():
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    
    # Create expenses table with user_id
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount FLOAT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            date DATE NOT NULL,
            recurring BOOLEAN NOT NULL DEFAULT FALSE,
            recurring_frequency TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create incomes table with user_id
    cur.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount FLOAT NOT NULL,
            source TEXT NOT NULL,
            date DATE NOT NULL,
            recurring BOOLEAN NOT NULL DEFAULT FALSE,
            recurring_frequency TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create budgets table with user_id
    cur.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount FLOAT NOT NULL,
            month TEXT NOT NULL,
            spent FLOAT NOT NULL DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create wishlist table with user_id
    cur.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price FLOAT NOT NULL,
            priority TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            target_date DATE,
            saved FLOAT NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create monthly_reports table with user_id
    cur.execute('''
        CREATE TABLE IF NOT EXISTS monthly_reports (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            total_income FLOAT NOT NULL,
            total_expenses FLOAT NOT NULL,
            savings_rate FLOAT NOT NULL,
            categories JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    cur.close()
    conn.close()

# Routes for expenses
@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC', (user_id,))
    expenses = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([dict(expense) for expense in expenses])

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    new_expense = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute('''
        INSERT INTO expenses (user_id, amount, description, category, date, recurring, recurring_frequency, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    ''', (
        user_id,
        new_expense['amount'],
        new_expense['description'],
        new_expense['category'],
        new_expense['date'],
        new_expense['recurring'],
        new_expense.get('recurringFrequency'),
        new_expense.get('notes')
    ))
    
    created_expense = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(dict(created_expense))

@app.route('/api/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM expenses WHERE id = %s AND user_id = %s RETURNING id', (id, user_id))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    
    if deleted:
        return jsonify({'message': 'Expense deleted successfully'})
    else:
        return jsonify({'error': 'Expense not found'}), 404

# Routes for incomes
@app.route('/api/incomes', methods=['GET'])
@jwt_required()
def get_incomes():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM incomes WHERE user_id = %s ORDER BY date DESC', (user_id,))
    incomes = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([dict(income) for income in incomes])

@app.route('/api/incomes', methods=['POST'])
@jwt_required()
def add_income():
    user_id = get_jwt_identity()
    new_income = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute('''
        INSERT INTO incomes (user_id, amount, source, date, recurring, recurring_frequency, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    ''', (
        user_id,
        new_income['amount'],
        new_income['source'],
        new_income['date'],
        new_income['recurring'],
        new_income.get('recurringFrequency'),
        new_income.get('notes')
    ))
    
    created_income = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(dict(created_income))

@app.route('/api/incomes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_income(id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM incomes WHERE id = %s AND user_id = %s RETURNING id', (id, user_id))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    
    if deleted:
        return jsonify({'message': 'Income deleted successfully'})
    else:
        return jsonify({'error': 'Income not found'}), 404

# Routes for budgets
@app.route('/api/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM budgets WHERE user_id = %s ORDER BY month DESC, category', (user_id,))
    budgets = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([dict(budget) for budget in budgets])

@app.route('/api/budgets', methods=['POST'])
@jwt_required()
def add_budget():
    user_id = get_jwt_identity()
    new_budget = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute('''
        INSERT INTO budgets (user_id, category, amount, month, spent, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    ''', (
        user_id,
        new_budget['category'],
        new_budget['amount'],
        new_budget['month'],
        new_budget.get('spent', 0),
        new_budget.get('notes')
    ))
    
    created_budget = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(dict(created_budget))

@app.route('/api/budgets/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_budget(id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM budgets WHERE id = %s AND user_id = %s RETURNING id', (id, user_id))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    
    if deleted:
        return jsonify({'message': 'Budget deleted successfully'})
    else:
        return jsonify({'error': 'Budget not found'}), 404

# Routes for wishlist
@app.route('/api/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM wishlist WHERE user_id = %s ORDER BY priority, price', (user_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([dict(item) for item in items])

@app.route('/api/wishlist', methods=['POST'])
@jwt_required()
def add_wishlist_item():
    user_id = get_jwt_identity()
    new_item = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute('''
        INSERT INTO wishlist (user_id, name, price, priority, url, notes, target_date, saved)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    ''', (
        user_id,
        new_item['name'],
        new_item['price'],
        new_item['priority'],
        new_item.get('url'),
        new_item.get('notes'),
        new_item.get('targetDate'),
        new_item.get('saved', 0)
    ))
    
    created_item = cur.fetchone()
    cur.close()
    conn.close()
    
    return jsonify(dict(created_item))

@app.route('/api/wishlist/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM wishlist WHERE id = %s AND user_id = %s RETURNING id', (id, user_id))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    
    if deleted:
        return jsonify({'message': 'Wishlist item deleted successfully'})
    else:
        return jsonify({'error': 'Wishlist item not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'finance-service'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
