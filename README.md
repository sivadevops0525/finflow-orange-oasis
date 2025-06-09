
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

## ⚙️ Configuration

### Changing Backend URL in Frontend

The frontend connects to the backend via the API URL configured in:

**File:** `frontend/src/contexts/AuthContext.tsx`

```typescript
// Backend API URL - Change this to your production backend URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
```

### For Production Deployment:

1. **Using Environment Variables (Recommended):**
   Set the `REACT_APP_API_URL` environment variable:
   ```bash
   export REACT_APP_API_URL=https://your-production-backend.com
   ```

2. **Direct Code Change:**
   Edit `frontend/src/contexts/AuthContext.tsx`:
   ```typescript
   const API_URL = 'https://your-production-backend.com';
   ```

3. **Docker Compose:**
   Update the `docker-compose.yml` file:
   ```yaml
   frontend:
     environment:
       - REACT_APP_API_URL=https://your-production-backend.com
   ```

## 🔒 Authentication

The application uses JWT-based authentication with hardcoded test credentials:
- Username: `testuser`
- Password: `testpass`

To add real authentication:
1. Replace the hardcoded credentials in `backend/app.py`
2. Implement database integration
3. Add proper user registration/management

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

## 🚀 Deployment

### Production Deployment Options:

1. **Docker Deployment:**
   - Deploy using Docker Compose on any Docker-compatible hosting
   - Update environment variables for production URLs

2. **Separate Deployment:**
   - Deploy backend to services like Heroku, Railway, or AWS
   - Deploy frontend to Netlify, Vercel, or similar
   - Update `REACT_APP_API_URL` to point to your backend

3. **Cloud Services:**
   - Use cloud providers like AWS, Google Cloud, or Azure
   - Configure environment variables accordingly

## 📝 Environment Variables

### Frontend (.env file or environment):
```
REACT_APP_API_URL=http://localhost:5001
```

### Backend:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
```

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
