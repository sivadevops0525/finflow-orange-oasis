
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://finflow:finflow123@postgres:5432/finflow_db')

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None

def require_auth(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token required'}), 401
        
        user = verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        request.user = user
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Mock data for test users
MOCK_DATA = {
    'expenses': [
        {'id': 1, 'amount': 50.00, 'description': 'Groceries', 'category': 'Food', 'date': '2024-01-15'},
        {'id': 2, 'amount': 30.00, 'description': 'Gas', 'category': 'Transportation', 'date': '2024-01-14'},
        {'id': 3, 'amount': 100.00, 'description': 'Utilities', 'category': 'Bills', 'date': '2024-01-13'}
    ],
    'income': [
        {'id': 1, 'amount': 3000.00, 'source': 'Salary', 'date': '2024-01-01'},
        {'id': 2, 'amount': 500.00, 'source': 'Freelance', 'date': '2024-01-10'}
    ],
    'budgets': [
        {'id': 1, 'category': 'Food', 'budgeted': 300.00, 'spent': 150.00},
        {'id': 2, 'category': 'Transportation', 'budgeted': 200.00, 'spent': 80.00}
    ]
}

@app.route('/expenses', methods=['GET', 'POST'])
@require_auth
def expenses():
    if request.method == 'GET':
        if request.user.get('type') == 'test':
            return jsonify(MOCK_DATA['expenses'])
        
        # Database logic for real users
        conn = get_db_connection()
        if not conn:
            return jsonify(MOCK_DATA['expenses'])  # Fallback to mock data
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC", (request.user['user_id'],))
            expenses = cur.fetchall()
            return jsonify([dict(expense) for expense in expenses])
        except:
            return jsonify(MOCK_DATA['expenses'])
        finally:
            cur.close()
            conn.close()
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if request.user.get('type') == 'test':
            new_expense = {
                'id': len(MOCK_DATA['expenses']) + 1,
                'amount': data['amount'],
                'description': data['description'],
                'category': data['category'],
                'date': data['date']
            }
            MOCK_DATA['expenses'].append(new_expense)
            return jsonify(new_expense), 201
        
        # Database logic for real users
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database not available'}), 503
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                "INSERT INTO expenses (user_id, amount, description, category, date) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (request.user['user_id'], data['amount'], data['description'], data['category'], data['date'])
            )
            expense = cur.fetchone()
            conn.commit()
            return jsonify(dict(expense)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()
            conn.close()

@app.route('/income', methods=['GET', 'POST'])
@require_auth
def income():
    if request.method == 'GET':
        if request.user.get('type') == 'test':
            return jsonify(MOCK_DATA['income'])
        
        conn = get_db_connection()
        if not conn:
            return jsonify(MOCK_DATA['income'])
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM income WHERE user_id = %s ORDER BY date DESC", (request.user['user_id'],))
            income_records = cur.fetchall()
            return jsonify([dict(record) for record in income_records])
        except:
            return jsonify(MOCK_DATA['income'])
        finally:
            cur.close()
            conn.close()
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if request.user.get('type') == 'test':
            new_income = {
                'id': len(MOCK_DATA['income']) + 1,
                'amount': data['amount'],
                'source': data['source'],
                'date': data['date']
            }
            MOCK_DATA['income'].append(new_income)
            return jsonify(new_income), 201
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database not available'}), 503
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                "INSERT INTO income (user_id, amount, source, date) VALUES (%s, %s, %s, %s) RETURNING *",
                (request.user['user_id'], data['amount'], data['source'], data['date'])
            )
            income_record = cur.fetchone()
            conn.commit()
            return jsonify(dict(income_record)), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()
            conn.close()

@app.route('/budget', methods=['GET'])
@require_auth
def budget():
    if request.user.get('type') == 'test':
        return jsonify(MOCK_DATA['budgets'])
    
    conn = get_db_connection()
    if not conn:
        return jsonify(MOCK_DATA['budgets'])
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM budgets WHERE user_id = %s", (request.user['user_id'],))
        budgets = cur.fetchall()
        return jsonify([dict(budget) for budget in budgets])
    except:
        return jsonify(MOCK_DATA['budgets'])
    finally:
        cur.close()
        conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'finance-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
