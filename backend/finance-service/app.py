
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

jwt = JWTManager(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'finflow_finance'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001')

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def validate_user_token(token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(f'{AUTH_SERVICE_URL}/api/auth/validate', headers=headers)
        if response.status_code == 200:
            return response.json().get('user')
        return None
    except:
        return None

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'service': 'finance-service'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# Expenses endpoints
@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, title, amount, category, date, description, created_at, updated_at
            FROM expenses WHERE user_id = %s ORDER BY date DESC
        """, (user_id,))
        
        expenses = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        for expense in expenses:
            if expense['date']:
                expense['date'] = expense['date'].isoformat()
            if expense['created_at']:
                expense['created_at'] = expense['created_at'].isoformat()
            if expense['updated_at']:
                expense['updated_at'] = expense['updated_at'].isoformat()
        
        return jsonify({'expenses': expenses}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title')
        amount = data.get('amount')
        category = data.get('category')
        date = data.get('date')
        description = data.get('description', '')
        
        if not all([title, amount, category, date]):
            return jsonify({'error': 'Title, amount, category and date are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO expenses (user_id, title, amount, category, date, description)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, title, amount, category, date, description, created_at
        """, (user_id, title, amount, category, date, description))
        
        expense = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        expense['date'] = expense['date'].isoformat()
        expense['created_at'] = expense['created_at'].isoformat()
        
        return jsonify({
            'message': 'Expense created successfully',
            'expense': expense
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if expense belongs to user
        cur.execute("SELECT id FROM expenses WHERE id = %s AND user_id = %s", (expense_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Expense not found'}), 404
        
        # Update expense
        cur.execute("""
            UPDATE expenses 
            SET title = %s, amount = %s, category = %s, date = %s, description = %s, updated_at = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, title, amount, category, date, description, updated_at
        """, (data.get('title'), data.get('amount'), data.get('category'), 
              data.get('date'), data.get('description'), datetime.utcnow(), expense_id, user_id))
        
        expense = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        expense['date'] = expense['date'].isoformat()
        expense['updated_at'] = expense['updated_at'].isoformat()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if expense belongs to user and delete
        cur.execute("DELETE FROM expenses WHERE id = %s AND user_id = %s RETURNING id", (expense_id, user_id))
        deleted_expense = cur.fetchone()
        
        if not deleted_expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Income endpoints
@app.route('/api/incomes', methods=['GET'])
@jwt_required()
def get_incomes():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, title, amount, source, date, description, created_at, updated_at
            FROM incomes WHERE user_id = %s ORDER BY date DESC
        """, (user_id,))
        
        incomes = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        for income in incomes:
            if income['date']:
                income['date'] = income['date'].isoformat()
            if income['created_at']:
                income['created_at'] = income['created_at'].isoformat()
            if income['updated_at']:
                income['updated_at'] = income['updated_at'].isoformat()
        
        return jsonify({'incomes': incomes}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/incomes', methods=['POST'])
@jwt_required()
def create_income():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title')
        amount = data.get('amount')
        source = data.get('source')
        date = data.get('date')
        description = data.get('description', '')
        
        if not all([title, amount, source, date]):
            return jsonify({'error': 'Title, amount, source and date are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO incomes (user_id, title, amount, source, date, description)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, title, amount, source, date, description, created_at
        """, (user_id, title, amount, source, date, description))
        
        income = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        income['date'] = income['date'].isoformat()
        income['created_at'] = income['created_at'].isoformat()
        
        return jsonify({
            'message': 'Income created successfully',
            'income': income
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/incomes/<int:income_id>', methods=['PUT'])
@jwt_required()
def update_income(income_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if income belongs to user
        cur.execute("SELECT id FROM incomes WHERE id = %s AND user_id = %s", (income_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Income not found'}), 404
        
        # Update income
        cur.execute("""
            UPDATE incomes 
            SET title = %s, amount = %s, source = %s, date = %s, description = %s, updated_at = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, title, amount, source, date, description, updated_at
        """, (data.get('title'), data.get('amount'), data.get('source'), 
              data.get('date'), data.get('description'), datetime.utcnow(), income_id, user_id))
        
        income = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        income['date'] = income['date'].isoformat()
        income['updated_at'] = income['updated_at'].isoformat()
        
        return jsonify({
            'message': 'Income updated successfully',
            'income': income
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/incomes/<int:income_id>', methods=['DELETE'])
@jwt_required()
def delete_income(income_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if income belongs to user and delete
        cur.execute("DELETE FROM incomes WHERE id = %s AND user_id = %s RETURNING id", (income_id, user_id))
        deleted_income = cur.fetchone()
        
        if not deleted_income:
            return jsonify({'error': 'Income not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Income deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Budget endpoints
@app.route('/api/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, category, amount, period, start_date, end_date, created_at, updated_at
            FROM budgets WHERE user_id = %s ORDER BY created_at DESC
        """, (user_id,))
        
        budgets = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        for budget in budgets:
            if budget['start_date']:
                budget['start_date'] = budget['start_date'].isoformat()
            if budget['end_date']:
                budget['end_date'] = budget['end_date'].isoformat()
            if budget['created_at']:
                budget['created_at'] = budget['created_at'].isoformat()
            if budget['updated_at']:
                budget['updated_at'] = budget['updated_at'].isoformat()
        
        return jsonify({'budgets': budgets}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/budgets', methods=['POST'])
@jwt_required()
def create_budget():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        category = data.get('category')
        amount = data.get('amount')
        period = data.get('period')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not all([category, amount, period, start_date]):
            return jsonify({'error': 'Category, amount, period and start_date are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO budgets (user_id, category, amount, period, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id, category, amount, period, start_date, end_date, created_at
        """, (user_id, category, amount, period, start_date, end_date))
        
        budget = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        budget['start_date'] = budget['start_date'].isoformat()
        if budget['end_date']:
            budget['end_date'] = budget['end_date'].isoformat()
        budget['created_at'] = budget['created_at'].isoformat()
        
        return jsonify({
            'message': 'Budget created successfully',
            'budget': budget
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/budgets/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if budget belongs to user
        cur.execute("SELECT id FROM budgets WHERE id = %s AND user_id = %s", (budget_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Budget not found'}), 404
        
        # Update budget
        cur.execute("""
            UPDATE budgets 
            SET category = %s, amount = %s, period = %s, start_date = %s, end_date = %s, updated_at = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, category, amount, period, start_date, end_date, updated_at
        """, (data.get('category'), data.get('amount'), data.get('period'), 
              data.get('start_date'), data.get('end_date'), datetime.utcnow(), budget_id, user_id))
        
        budget = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        budget['start_date'] = budget['start_date'].isoformat()
        if budget['end_date']:
            budget['end_date'] = budget['end_date'].isoformat()
        budget['updated_at'] = budget['updated_at'].isoformat()
        
        return jsonify({
            'message': 'Budget updated successfully',
            'budget': budget
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if budget belongs to user and delete
        cur.execute("DELETE FROM budgets WHERE id = %s AND user_id = %s RETURNING id", (budget_id, user_id))
        deleted_budget = cur.fetchone()
        
        if not deleted_budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Budget deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Wishlist endpoints
@app.route('/api/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, title, amount, priority, target_date, description, is_completed, created_at, updated_at
            FROM wishlist WHERE user_id = %s ORDER BY priority DESC, created_at DESC
        """, (user_id,))
        
        wishlist = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        for item in wishlist:
            if item['target_date']:
                item['target_date'] = item['target_date'].isoformat()
            if item['created_at']:
                item['created_at'] = item['created_at'].isoformat()
            if item['updated_at']:
                item['updated_at'] = item['updated_at'].isoformat()
        
        return jsonify({'wishlist': wishlist}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wishlist', methods=['POST'])
@jwt_required()
def create_wishlist_item():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title')
        amount = data.get('amount')
        priority = data.get('priority', 3)
        target_date = data.get('target_date')
        description = data.get('description', '')
        
        if not all([title, amount]):
            return jsonify({'error': 'Title and amount are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO wishlist (user_id, title, amount, priority, target_date, description)
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id, title, amount, priority, target_date, description, is_completed, created_at
        """, (user_id, title, amount, priority, target_date, description))
        
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        if item['target_date']:
            item['target_date'] = item['target_date'].isoformat()
        item['created_at'] = item['created_at'].isoformat()
        
        return jsonify({
            'message': 'Wishlist item created successfully',
            'item': item
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wishlist/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_wishlist_item(item_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if item belongs to user
        cur.execute("SELECT id FROM wishlist WHERE id = %s AND user_id = %s", (item_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Wishlist item not found'}), 404
        
        # Update item
        cur.execute("""
            UPDATE wishlist 
            SET title = %s, amount = %s, priority = %s, target_date = %s, description = %s, 
                is_completed = %s, updated_at = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, title, amount, priority, target_date, description, is_completed, updated_at
        """, (data.get('title'), data.get('amount'), data.get('priority'), 
              data.get('target_date'), data.get('description'), data.get('is_completed', False),
              datetime.utcnow(), item_id, user_id))
        
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert date objects to strings
        if item['target_date']:
            item['target_date'] = item['target_date'].isoformat()
        item['updated_at'] = item['updated_at'].isoformat()
        
        return jsonify({
            'message': 'Wishlist item updated successfully',
            'item': item
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wishlist/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(item_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if item belongs to user and delete
        cur.execute("DELETE FROM wishlist WHERE id = %s AND user_id = %s RETURNING id", (item_id, user_id))
        deleted_item = cur.fetchone()
        
        if not deleted_item:
            return jsonify({'error': 'Wishlist item not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Wishlist item deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
