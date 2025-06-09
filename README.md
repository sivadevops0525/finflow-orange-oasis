
# FinFlow - Personal Financial Manager

A beautiful and intuitive personal finance management application built with React and Flask.

## Features

- 📊 Dashboard with financial overview
- 💰 Income and expense tracking
- 🎯 Budget management
- 💝 Wishlist functionality
- 📈 Financial reports and analytics
- 🔐 Secure authentication

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Running the Application

1. **Start the Backend** (in one terminal):
   ```bash
   python start-backend.py
   ```
   Or manually:
   ```bash
   cd backend/simple-auth
   pip install -r requirements.txt
   python app.py
   ```

2. **Start the Frontend** (in another terminal):
   ```bash
   npm install
   npm run dev
   ```

3. **Access the Application**:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5001

### Test Credentials
- Username: `testuser`
- Password: `testpass`

## Project Structure

```
├── src/                    # Frontend React application
│   ├── components/         # Reusable UI components
│   ├── pages/             # Application pages
│   ├── contexts/          # React contexts
│   └── ...
├── backend/               # Backend services
│   └── simple-auth/       # Authentication service
└── ...
```

## Technologies Used

- **Frontend**: React, TypeScript, Tailwind CSS, Shadcn/ui
- **Backend**: Flask, PyJWT
- **Charts**: Recharts
- **Icons**: Lucide React

## Development

The application is designed to be easily extensible. You can:
- Replace test credentials with a real database
- Add more financial features
- Customize the UI theme
- Integrate with external APIs

## License

MIT License
