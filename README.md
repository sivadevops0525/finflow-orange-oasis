# FinFlow - Personal Financial Manager

A clean and functional personal finance management application built with React and Flask.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed on your system

### Run the Application
```bash
# Clone this repository
git clone <your-repo-url>
cd finflow

# Start the application with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5001
```

### Test Credentials
```
Username: testuser
Password: testpass
```

## 📁 Project Structure

```
finflow/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Application pages
│   │   ├── contexts/        # React contexts (AuthContext)
│   │   └── ...
│   ├── Dockerfile
│   └── package.json
├── backend/                  # Flask backend API
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── docker-compose.yml       # Docker Compose configuration
└── README.md
```

## 🔧 Local Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on: http://localhost:5001

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: http://localhost:5173

## 🎯 Features

- ✅ User Authentication (Login/Logout)
- ✅ Dashboard Overview
- ✅ Expense Tracking
- ✅ Income Management
- ✅ Budget Planning
- ✅ Wishlist
- ✅ Financial Reports
- ✅ Responsive Design
- ✅ Docker Support

## 🛠️ Tech Stack

- **Frontend:** React 18, TypeScript, Tailwind CSS, Shadcn/ui
- **Backend:** Flask, PyJWT
- **Authentication:** JWT tokens
- **Charts:** Recharts
- **Icons:** Lucide React
- **Deployment:** Docker, Docker Compose

## 📞 Support

For issues or questions:
1. Check the console logs in your browser
2. Verify backend is running on the correct port
3. Ensure frontend is pointing to the correct backend URL
4. Check Docker containers are running: `docker-compose ps`

---

**Note:** This is a demo application with hardcoded credentials. For production use, implement proper user management, database integration, and security measures.