
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras
import bcrypt
import os
from datetime import timedelta, datetime
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import secrets
import re

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'finflow_auth'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database
def init_db():
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    
    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Create password reset tokens table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            token VARCHAR(255) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    cur.close()
    conn.close()

# Utility functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def send_reset_email(email, token):
    # This is a basic implementation - replace with your email service
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_username, smtp_password]):
            print("SMTP credentials not configured")
            return False
        
        msg = MimeMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = "FinFlow - Password Reset"
        
        reset_link = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={token}"
        body = f"""
        Hello,
        
        You requested a password reset for your FinFlow account.
        Click the link below to reset your password:
        
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        FinFlow Team
        """
        
        msg.attach(MimeText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validation
        if not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Check if user already exists
        cur.execute('SELECT id FROM users WHERE username = %s OR email = %s', 
                   (data['username'], data['email']))
        if cur.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Hash password and create user
        password_hash = hash_password(data['password'])
        
        cur.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, username, email, first_name, last_name, created_at
        ''', (
            data['username'],
            data['email'],
            password_hash,
            data.get('first_name'),
            data.get('last_name')
        ))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        # Create access token
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'created_at': user['created_at'].isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ('username', 'password')):
            return jsonify({'error': 'Missing username or password'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find user by username or email
        cur.execute('''
            SELECT id, username, email, password_hash, first_name, last_name, is_active
            FROM users 
            WHERE (username = %s OR email = %s) AND is_active = TRUE
        ''', (data['username'], data['username']))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or not verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        
        if 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find user by email
        cur.execute('SELECT id, email FROM users WHERE email = %s AND is_active = TRUE', (data['email'],))
        user = cur.fetchone()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)
            
            # Save token to database
            cur.execute('''
                INSERT INTO password_reset_tokens (user_id, token, expires_at)
                VALUES (%s, %s, %s)
            ''', (user['id'], token, expires_at))
            
            # Send reset email
            if send_reset_email(user['email'], token):
                cur.close()
                conn.close()
                return jsonify({'message': 'Password reset email sent'}), 200
            else:
                cur.close()
                conn.close()
                return jsonify({'error': 'Failed to send reset email'}), 500
        
        cur.close()
        conn.close()
        
        # Always return success to prevent email enumeration
        return jsonify({'message': 'If email exists, reset link has been sent'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ('token', 'new_password')):
            return jsonify({'error': 'Missing token or new password'}), 400
        
        if len(data['new_password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Find valid token
        cur.execute('''
            SELECT prt.id, prt.user_id, u.email
            FROM password_reset_tokens prt
            JOIN users u ON prt.user_id = u.id
            WHERE prt.token = %s AND prt.expires_at > NOW() AND prt.used = FALSE
        ''', (data['token'],))
        
        token_data = cur.fetchone()
        
        if not token_data:
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        # Update password
        password_hash = hash_password(data['new_password'])
        
        cur.execute('UPDATE users SET password_hash = %s WHERE id = %s', 
                   (password_hash, token_data['user_id']))
        
        # Mark token as used
        cur.execute('UPDATE password_reset_tokens SET used = TRUE WHERE id = %s', 
                   (token_data['id'],))
        
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute('''
            SELECT id, username, email, first_name, last_name, created_at
            FROM users WHERE id = %s AND is_active = TRUE
        ''', (user_id,))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'created_at': user['created_at'].isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ('current_password', 'new_password')):
            return jsonify({'error': 'Missing current or new password'}), 400
        
        if len(data['new_password']) < 6:
            return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Verify current password
        cur.execute('SELECT password_hash FROM users WHERE id = %s', (user_id,))
        user = cur.fetchone()
        
        if not user or not verify_password(data['current_password'], user['password_hash']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Update password
        password_hash = hash_password(data['new_password'])
        cur.execute('UPDATE users SET password_hash = %s WHERE id = %s', 
                   (password_hash, user_id))
        
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'auth-service'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
