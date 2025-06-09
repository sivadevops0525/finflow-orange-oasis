
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Service URLs
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:5001')
FINANCE_SERVICE_URL = os.getenv('FINANCE_SERVICE_URL', 'http://finance-service:5002')

def proxy_request(service_url, path, method='GET'):
    """Proxy request to microservice"""
    try:
        url = f"{service_url}{path}"
        headers = {}
        
        # Forward authorization header
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        
        if method == 'GET':
            response = requests.get(url, headers=headers, params=request.args)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=request.get_json())
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=request.get_json())
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Service unavailable: {str(e)}'}), 503

# Auth service routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    return proxy_request(AUTH_SERVICE_URL, '/login', 'POST')

@app.route('/api/auth/register', methods=['POST'])
def register():
    return proxy_request(AUTH_SERVICE_URL, '/register', 'POST')

@app.route('/api/auth/verify', methods=['POST'])
def verify():
    return proxy_request(AUTH_SERVICE_URL, '/verify', 'POST')

# Finance service routes
@app.route('/api/finance/expenses', methods=['GET', 'POST'])
def expenses():
    return proxy_request(FINANCE_SERVICE_URL, '/expenses', request.method)

@app.route('/api/finance/income', methods=['GET', 'POST'])
def income():
    return proxy_request(FINANCE_SERVICE_URL, '/income', request.method)

@app.route('/api/finance/budget', methods=['GET'])
def budget():
    return proxy_request(FINANCE_SERVICE_URL, '/budget', 'GET')

# Health check
@app.route('/health', methods=['GET'])
def health():
    try:
        auth_health = requests.get(f"{AUTH_SERVICE_URL}/health", timeout=5)
        finance_health = requests.get(f"{FINANCE_SERVICE_URL}/health", timeout=5)
        
        return jsonify({
            'status': 'healthy',
            'services': {
                'auth': auth_health.json() if auth_health.status_code == 200 else 'unhealthy',
                'finance': finance_health.json() if finance_health.status_code == 200 else 'unhealthy'
            }
        })
    except:
        return jsonify({'status': 'unhealthy'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
