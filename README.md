
# FinFlow - Personal Finance Management System

A modern, microservices-based personal finance management application built with React frontend and Python Flask backend.

## Architecture

### Frontend (Microfrontends)
- **Main App**: React application with TypeScript, Tailwind CSS, and shadcn/ui components
- **Authentication**: Login, Register, Forgot Password, Reset Password
- **Financial Management**: Expenses, Income, Budget, Wishlist tracking
- **Reports**: Financial analytics and visualizations

### Backend (Microservices)
- **Auth Service**: User authentication, registration, password management
- **Finance Service**: Expenses, income, budget, and wishlist management
- **API Gateway**: Central entry point that routes requests to appropriate services
- **Database**: PostgreSQL with separate databases for auth and finance data

## Project Structure

```
finflow/
├── frontend/
│   └── main-app/              # React frontend application
│       ├── src/
│       │   ├── components/    # Reusable UI components
│       │   ├── pages/         # Application pages
│       │   ├── contexts/      # React contexts (Auth, etc.)
│       │   └── lib/           # Utilities and configurations
│       ├── Dockerfile
│       └── package.json
├── backend/
│   ├── auth-service/          # Authentication microservice
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── finance-service/       # Finance management microservice
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── api-gateway/           # API Gateway
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── init-db.sql           # Database initialization
├── docker-compose.yml        # Container orchestration
└── .env.example              # Environment variables template
```

## Features

### Authentication
- User registration and login
- Password reset via email
- JWT token-based authentication
- Profile management

### Financial Management
- **Expenses**: Track daily expenses with categories
- **Income**: Record income from various sources
- **Budget**: Set and monitor budgets by category
- **Wishlist**: Track financial goals and priorities
- **Reports**: Visualize spending patterns and financial health

### Technical Features
- Microservices architecture
- RESTful APIs
- JWT authentication
- PostgreSQL database
- Docker containerization
- Responsive design
- Real-time data updates

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Environment Setup
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your configurations:
   - Database credentials
   - JWT secret key
   - Email settings (for password reset)

### Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd finflow
   ```

2. Start all services with Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:5000
   - Auth Service: http://localhost:5001
   - Finance Service: http://localhost:5002
   - Database: localhost:5432

### Service Health Check
- API Gateway: http://localhost:5000/health
- Auth Service: http://localhost:5001/health
- Finance Service: http://localhost:5002/health

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token
- `POST /api/auth/change-password` - Change password (authenticated)
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Finance Endpoints
- `GET /api/expenses` - Get user expenses
- `POST /api/expenses` - Create expense
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/incomes` - Get user incomes
- `POST /api/incomes` - Create income
- `PUT /api/incomes/{id}` - Update income
- `DELETE /api/incomes/{id}` - Delete income
- `GET /api/budgets` - Get user budgets
- `POST /api/budgets` - Create budget
- `PUT /api/budgets/{id}` - Update budget
- `DELETE /api/budgets/{id}` - Delete budget
- `GET /api/wishlist` - Get user wishlist
- `POST /api/wishlist` - Create wishlist item
- `PUT /api/wishlist/{id}` - Update wishlist item
- `DELETE /api/wishlist/{id}` - Delete wishlist item

## Development

### Frontend Development
```bash
cd frontend/main-app
npm install
npm run dev
```

### Backend Development
Each service can be run independently:

```bash
# Auth Service
cd backend/auth-service
pip install -r requirements.txt
python app.py

# Finance Service
cd backend/finance-service
pip install -r requirements.txt
python app.py

# API Gateway
cd backend/api-gateway
pip install -r requirements.txt
python app.py
```

## Deployment

The application is containerized and can be deployed using Docker Compose on any Docker-compatible platform:

1. Production deployment with Docker Compose
2. Kubernetes deployment (requires creating K8s manifests)
3. Cloud deployment (AWS ECS, Google Cloud Run, etc.)

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation
- SQL injection prevention
- Environment-based configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
