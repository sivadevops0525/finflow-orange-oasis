
# FinFlow - Microservices Financial Management Application

A modern, production-grade financial management application built with microservices architecture.

## Architecture Overview

### Backend Microservices
- **API Gateway** (Port 5000): Routes requests to appropriate services
- **Auth Service** (Port 5001): Handles user authentication and authorization
- **Finance Service** (Port 5002): Manages financial data (expenses, income, budgets, wishlist)
- **PostgreSQL Database**: Separate databases for each service

### Frontend Microfrontends
- **Main App** (Port 3000): React application with modern UI

## Features

### Authentication
- User registration and login
- Password reset via email
- JWT-based authentication
- Password change functionality
- Secure session management

### Financial Management
- Expense tracking with categories
- Income management
- Budget planning and monitoring
- Wishlist with savings goals
- Financial reports and analytics

### Technical Features
- Microservices architecture
- Docker containerization
- PostgreSQL with separate databases
- JWT authentication
- RESTful APIs
- Modern React frontend with TypeScript
- Responsive design with Tailwind CSS
- Real-time data visualization with Recharts

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. Clone the repository
2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start all services:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:5000
   - Auth Service: http://localhost:5001
   - Finance Service: http://localhost:5002

### Local Development

#### Backend Services

1. **Auth Service**:
   ```bash
   cd backend/auth-service
   pip install -r requirements.txt
   python app.py
   ```

2. **Finance Service**:
   ```bash
   cd backend/finance-service
   pip install -r requirements.txt
   python app.py
   ```

3. **API Gateway**:
   ```bash
   cd backend/api-gateway
   pip install -r requirements.txt
   python app.py
   ```

#### Frontend

```bash
cd frontend/main-app
npm install
npm run dev
```

## Environment Configuration

### Required Environment Variables

**Database:**
- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password

**Authentication:**
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `FRONTEND_URL`: Frontend URL for password reset links

**Email (for password reset):**
- `SMTP_SERVER`: SMTP server address
- `SMTP_PORT`: SMTP server port
- `SMTP_USERNAME`: Email username
- `SMTP_PASSWORD`: Email password

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/change-password` - Change password

### Finance Endpoints
- `GET /api/expenses` - Get user expenses
- `POST /api/expenses` - Create expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/incomes` - Get user incomes
- `POST /api/incomes` - Create income
- `DELETE /api/incomes/{id}` - Delete income
- `GET /api/budgets` - Get user budgets
- `POST /api/budgets` - Create budget
- `DELETE /api/budgets/{id}` - Delete budget
- `GET /api/wishlist` - Get user wishlist
- `POST /api/wishlist` - Create wishlist item
- `DELETE /api/wishlist/{id}` - Delete wishlist item

## Database Schema

### Auth Service Database (finflow_auth)
- `users` - User account information
- `password_reset_tokens` - Password reset tokens

### Finance Service Database (finflow_finance)
- `expenses` - User expenses
- `incomes` - User income sources
- `budgets` - User budgets
- `wishlist` - User wishlist items
- `monthly_reports` - Financial reports

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection prevention
- CORS configuration
- Input validation
- Secure password reset flow

## Deployment

### Production Deployment with Docker

1. Update environment variables for production
2. Build and deploy:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Health Monitoring

Health check endpoints are available:
- API Gateway: `GET /health`
- Auth Service: `GET /health`
- Finance Service: `GET /health`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
