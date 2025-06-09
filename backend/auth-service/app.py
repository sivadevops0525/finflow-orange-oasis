
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import hashlib
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://finflow:finflow123@postgres:5432/finflow_db')

# Test credentials (work without DB)
TEST_CREDENTIALS = {
    'testuser': 'testpass123',
    'admin': 'admin123',
    'demo': 'demo123'
}

def get_db_connection():
    """Get database connection with error handling"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_test_credentials(username, password):
    """Verify against test credentials"""
    return username in TEST_CREDENTIALS and TEST_CREDENTIALS[username] == password

def verify_db_credentials(username, password):
    """Verify against database credentials"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        hashed_password = hash_password(password)
        
        cur.execute(
            "SELECT id, username, email FROM users WHERE username = %s AND password = %s",
            (username, hashed_password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Database query failed: {e}")
        return False

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check test credentials first
        if verify_test_credentials(username, password):
            token = jwt.encode({
                'user_id': username,
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'type': 'test'
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'id': username,
                    'username': username,
                    'email': f"{username}@test.com",
                    'type': 'test'
                }
            })
        
        # Check database credentials
        db_user = verify_db_credentials(username, password)
        if db_user:
            token = jwt.encode({
                'user_id': db_user['id'],
                'username': db_user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'type': 'db'
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'id': db_user['id'],
                    'username': db_user['username'],
                    'email': db_user['email'],
                    'type': 'db'
                }
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password or not email:
            return jsonify({'error': 'Username, password, and email required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database not available. Try test credentials instead.'}), 503
        
        try:
            cur = conn.cursor()
            hashed_password = hash_password(password)
            
            # Check if user exists
            cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone():
                return jsonify({'error': 'User already exists'}), 409
            
            # Create user
            cur.execute(
                "INSERT INTO users (username, email, password, created_at) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, hashed_password, datetime.datetime.utcnow())
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            
            token = jwt.encode({
                'user_id': user_id,
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'type': 'db'
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'type': 'db'
                }
            }), 201
            
        finally:
            cur.close()
            conn.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token required'}), 401
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'user': payload}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'auth-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
