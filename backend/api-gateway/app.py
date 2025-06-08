
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Service URLs
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001')
FINANCE_SERVICE_URL = os.getenv('FINANCE_SERVICE_URL', 'http://localhost:5002')

def forward_request(service_url, path, method='GET'):
    """Forward request to the appropriate microservice"""
    url = f"{service_url}{path}"
    headers = {}
    
    # Forward authorization header
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    
    headers['Content-Type'] = 'application/json'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=request.args)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=request.get_json())
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=request.get_json())
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return jsonify({'error': 'Method not allowed'}), 405
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Service unavailable: {str(e)}'}), 503

# Auth service routes
@app.route('/api/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path):
    return forward_request(AUTH_SERVICE_URL, f'/api/auth/{path}', request.method)

# Finance service routes
@app.route('/api/expenses', methods=['GET', 'POST'])
@app.route('/api/expenses/<int:id>', methods=['PUT', 'DELETE'])
def expenses_proxy(id=None):
    path = f'/api/expenses/{id}' if id else '/api/expenses'
    return forward_request(FINANCE_SERVICE_URL, path, request.method)

@app.route('/api/incomes', methods=['GET', 'POST'])
@app.route('/api/incomes/<int:id>', methods=['PUT', 'DELETE'])
def incomes_proxy(id=None):
    path = f'/api/incomes/{id}' if id else '/api/incomes'
    return forward_request(FINANCE_SERVICE_URL, path, request.method)

@app.route('/api/budgets', methods=['GET', 'POST'])
@app.route('/api/budgets/<int:id>', methods=['PUT', 'DELETE'])
def budgets_proxy(id=None):
    path = f'/api/budgets/{id}' if id else '/api/budgets'
    return forward_request(FINANCE_SERVICE_URL, path, request.method)

@app.route('/api/wishlist', methods=['GET', 'POST'])
@app.route('/api/wishlist/<int:id>', methods=['PUT', 'DELETE'])
def wishlist_proxy(id=None):
    path = f'/api/wishlist/{id}' if id else '/api/wishlist'
    return forward_request(FINANCE_SERVICE_URL, path, request.method)

@app.route('/health', methods=['GET'])
def health_check():
    # Check health of all services
    services = {
        'api-gateway': 'healthy',
        'auth-service': 'unknown',
        'finance-service': 'unknown'
    }
    
    try:
        auth_health = requests.get(f'{AUTH_SERVICE_URL}/health', timeout=5)
        services['auth-service'] = 'healthy' if auth_health.status_code == 200 else 'unhealthy'
    except:
        services['auth-service'] = 'unhealthy'
    
    try:
        finance_health = requests.get(f'{FINANCE_SERVICE_URL}/health', timeout=5)
        services['finance-service'] = 'healthy' if finance_health.status_code == 200 else 'unhealthy'
    except:
        services['finance-service'] = 'unhealthy'
    
    return jsonify({'status': 'healthy', 'services': services}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
