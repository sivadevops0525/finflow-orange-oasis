
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import os
from datetime import timedelta, datetime
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'finflow_auth'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def send_reset_email(email, reset_token):
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        
        if not smtp_username or not smtp_password:
            return False
        
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = "Password Reset - FinFlow"
        
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"
        body = f"""
        Hi,
        
        You requested a password reset for your FinFlow account.
        
        Click the link below to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        FinFlow Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'service': 'auth-service'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email and password are required'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 400
        
        # Create user
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (%s, %s, %s, %s) RETURNING id, username, email, full_name, created_at
        """, (username, email, password_hash, full_name))
        
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Create access token
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'created_at': user['created_at'].isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find user by username or email
        cur.execute("""
            SELECT id, username, email, password_hash, full_name, is_active
            FROM users WHERE username = %s OR email = %s
        """, (username, username))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or not user['is_active']:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if not user:
            # Don't reveal if email exists or not
            return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # Save reset token
        cur.execute("""
            UPDATE users SET reset_token = %s, reset_token_expires = %s 
            WHERE email = %s
        """, (reset_token, expires_at, email))
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Send email
        if send_reset_email(email, reset_token):
            return jsonify({'message': 'Password reset link sent to your email'}), 200
        else:
            return jsonify({'error': 'Failed to send reset email'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find user with valid token
        cur.execute("""
            SELECT id FROM users 
            WHERE reset_token = %s AND reset_token_expires > %s
        """, (token, datetime.utcnow()))
        
        user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        # Hash new password
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password and clear reset token
        cur.execute("""
            UPDATE users 
            SET password_hash = %s, reset_token = NULL, reset_token_expires = NULL, updated_at = %s
            WHERE id = %s
        """, (password_hash, datetime.utcnow(), user['id']))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password are required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get current password hash
        cur.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Hash new password
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password
        cur.execute("""
            UPDATE users SET password_hash = %s, updated_at = %s WHERE id = %s
        """, (password_hash, datetime.utcnow(), user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, email, full_name, created_at, updated_at
            FROM users WHERE id = %s
        """, (user_id,))
        
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
                'full_name': user['full_name'],
                'created_at': user['created_at'].isoformat(),
                'updated_at': user['updated_at'].isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        full_name = data.get('full_name')
        email = data.get('email')
        
        if not full_name and not email:
            return jsonify({'error': 'At least one field is required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if email is already taken by another user
        if email:
            cur.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
            if cur.fetchone():
                return jsonify({'error': 'Email already exists'}), 400
        
        # Update profile
        if full_name and email:
            cur.execute("""
                UPDATE users SET full_name = %s, email = %s, updated_at = %s 
                WHERE id = %s
            """, (full_name, email, datetime.utcnow(), user_id))
        elif full_name:
            cur.execute("""
                UPDATE users SET full_name = %s, updated_at = %s 
                WHERE id = %s
            """, (full_name, datetime.utcnow(), user_id))
        elif email:
            cur.execute("""
                UPDATE users SET email = %s, updated_at = %s 
                WHERE id = %s
            """, (email, datetime.utcnow(), user_id))
        
        conn.commit()
        
        # Get updated user data
        cur.execute("""
            SELECT id, username, email, full_name, created_at, updated_at
            FROM users WHERE id = %s
        """, (user_id,))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'created_at': user['created_at'].isoformat(),
                'updated_at': user['updated_at'].isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/validate', methods=['POST'])
@jwt_required()
def validate_token():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, email, full_name
            FROM users WHERE id = %s AND is_active = TRUE
        """, (user_id,))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
