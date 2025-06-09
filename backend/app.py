
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# Configuration
SECRET_KEY = 'your-secret-key-here'

# Test credentials - Replace with your database logic
TEST_USER = {
    'username': 'testuser',
    'password': 'testpass',
    'email': 'test@finflow.com'
}

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check test credentials
        if username == TEST_USER['username'] and password == TEST_USER['password']:
            token = jwt.encode({
                'user_id': TEST_USER['username'],
                'username': TEST_USER['username'],
                'email': TEST_USER['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user': {
                    'username': TEST_USER['username'],
                    'email': TEST_USER['email']
                }
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify', methods=['POST'])
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
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
