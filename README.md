
# FinFlow - Personal Financial Manager

A microservices-based financial management application with React frontend and Python backend.

## 🏗️ Architecture

This application follows a microservices architecture:

### Frontend
- **Main App**: React application with Vite, TypeScript, and Tailwind CSS

### Backend Services
- **API Gateway**: Routes requests to appropriate microservices (Port 5000)
- **Auth Service**: Handles authentication and user management (Port 5001)
- **Finance Service**: Manages financial data (expenses, income, budget) (Port 5002)
- **PostgreSQL Database**: Data persistence (Port 5432)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Running the Application

1. Clone the repository:
```bash
git clone <your-repo-url>
cd finflow
```

2. Start all services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:5000
- Auth Service: http://localhost:5001
- Finance Service: http://localhost:5002

## 🔐 Authentication

### Test Credentials (No Database Required)
These credentials work without database connection:

- Username: `testuser` | Password: `testpass123`
- Username: `admin` | Password: `admin123`
- Username: `demo` | Password: `demo123`

### Database Users
For production users, register through the app. User data will be stored in PostgreSQL.

## 📁 Project Structure

```
finflow/
├── frontend/
│   └── main-app/                 # React frontend
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── backend/
│   ├── auth-service/             # Authentication microservice
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── finance-service/          # Finance data microservice
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── api-gateway/              # API Gateway
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── init-db.sql              # Database initialization
├── docker-compose.yml           # Orchestration
└── README.md
```

## 🛠️ Development

### Environment Variables
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### Running Individual Services

#### Backend Services
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

#### Frontend
```bash
cd frontend/main-app
npm install
npm run dev
```

## 🔄 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/verify` - Token verification

### Finance
- `GET /api/finance/expenses` - Get user expenses
- `POST /api/finance/expenses` - Add new expense
- `GET /api/finance/income` - Get user income
- `POST /api/finance/income` - Add new income
- `GET /api/finance/budget` - Get user budget

## 🗄️ Database

### Tables
- `users` - User accounts
- `expenses` - User expenses
- `income` - User income records
- `budgets` - Budget categories
- `wishlist` - User wishlist items

### Connection
- Host: localhost (or postgres in Docker)
- Port: 5432
- Database: finflow_db
- Username: finflow
- Password: finflow123

## 🔧 Features

- ✅ User Authentication (Login/Register)
- ✅ Test Credentials Support
- ✅ Expense Tracking
- ✅ Income Management
- ✅ Budget Planning
- ✅ Wishlist Management
- ✅ Financial Reports
- ✅ Responsive Design
- ✅ Microservices Architecture
- ✅ Docker Containerization

## 🚀 Deployment

The application is containerized and can be deployed to any Docker-compatible platform:

- AWS ECS/EKS
- Google Cloud Run/GKE
- Azure Container Instances/AKS
- Digital Ocean App Platform
- Heroku (with Docker)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.
