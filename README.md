# FinFlow - Microfrontends Architecture

FinFlow is a personal finance management application built using a microfrontends architecture. Each feature is developed as an independent, deployable service that can be developed, tested, and deployed separately.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Nginx (Port 80)                      │
│                     Reverse Proxy                           │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │ Shell App    │ │Dashboard  │ │  Expenses   │
        │ (Port 3000)  │ │(Port 3001)│ │ (Port 3002) │
        └──────────────┘ └───────────┘ └─────────────┘
                │               │               │
        ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   Income     │ │  Budget   │ │  Wishlist   │
        │ (Port 3003)  │ │(Port 3004)│ │ (Port 3005) │
        └──────────────┘ └───────────┘ └─────────────┘
                │               │
        ┌───────▼──────┐ ┌─────▼─────┐
        │   Reports    │ │   Shared  │
        │ (Port 3006)  │ │Components │
        └──────────────┘ └───────────┘
```

## Project Structure

```
finflow/
├── docker-compose.yml                 # Main orchestration file
├── microfrontends/
│   ├── shell/                        # Main shell application
│   │   ├── src/
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── vite.config.ts
│   ├── dashboard/                    # Dashboard microfrontend
│   ├── expenses/                     # Expenses microfrontend
│   ├── income/                       # Income microfrontend
│   ├── budget/                       # Budget microfrontend
│   ├── wishlist/                     # Wishlist microfrontend
│   └── reports/                      # Reports microfrontend
├── shared/                           # Shared components and utilities
│   ├── components/                   # Reusable UI components
│   ├── utils/                        # Utility functions
│   └── types/                        # TypeScript type definitions
└── infrastructure/
    ├── nginx/                        # Nginx configuration
    └── docker/                       # Docker configurations
```

## Microfrontends

### 1. Shell Application (Port 3000)
- **Purpose**: Main container application that orchestrates all microfrontends
- **Responsibilities**:
  - Routing between microfrontends
  - Shared navigation (sidebar)
  - Authentication (future)
  - Global state management
  - Loading and error handling for microfrontends

### 2. Dashboard (Port 3001)
- **Purpose**: Financial overview and analytics
- **Features**:
  - Income vs expenses charts
  - Savings rate tracking
  - Recent transactions
  - Budget overview
  - Financial health metrics

### 3. Expenses (Port 3002)
- **Purpose**: Expense tracking and management
- **Features**:
  - Add/edit/delete expenses
  - Categorization
  - Recurring expenses
  - Expense analytics

### 4. Income (Port 3003)
- **Purpose**: Income tracking and management
- **Features**:
  - Add/edit/delete income sources
  - Recurring income tracking
  - Income analytics

### 5. Budget (Port 3004)
- **Purpose**: Budget planning and monitoring
- **Features**:
  - Create and manage budgets
  - Budget vs actual spending
  - Budget alerts and notifications
  - Monthly/yearly budget planning

### 6. Wishlist (Port 3005)
- **Purpose**: Savings goals and wishlist management
- **Features**:
  - Add items to wishlist
  - Set savings goals
  - Track progress
  - Priority management

### 7. Reports (Port 3006)
- **Purpose**: Advanced reporting and analytics
- **Features**:
  - Detailed financial reports
  - Custom date ranges
  - Export functionality
  - Trend analysis

## Shared Resources

### Components
- UI components (buttons, cards, forms, etc.)
- Layout components (headers, sidebars)
- Chart components
- Common dialogs and modals

### Utilities
- Date formatting
- Currency formatting
- Validation functions
- API helpers

### Types
- TypeScript interfaces
- Common data models
- API response types

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- npm or yarn

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finflow
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Main application: http://localhost
   - Individual microfrontends:
     - Shell: http://localhost:3000
     - Dashboard: http://localhost:3001
     - Expenses: http://localhost:3002
     - Income: http://localhost:3003
     - Budget: http://localhost:3004
     - Wishlist: http://localhost:3005
     - Reports: http://localhost:3006

### Local Development

1. **Install dependencies for each microfrontend**
   ```bash
   cd microfrontends/shell && npm install
   cd ../dashboard && npm install
   cd ../expenses && npm install
   # ... repeat for all microfrontends
   ```

2. **Start development servers**
   ```bash
   # Terminal 1 - Shell
   cd microfrontends/shell && npm run dev

   # Terminal 2 - Dashboard
   cd microfrontends/dashboard && npm run dev

   # Terminal 3 - Expenses
   cd microfrontends/expenses && npm run dev

   # ... and so on for each microfrontend
   ```

## Deployment

### Production Deployment

1. **Build and deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml up --build -d
   ```

2. **Scale individual services**
   ```bash
   docker-compose up --scale dashboard=3 --scale expenses=2
   ```

### Individual Service Deployment

Each microfrontend can be deployed independently:

```bash
# Build specific service
docker-compose build dashboard

# Deploy specific service
docker-compose up dashboard
```

## Benefits of This Architecture

### 1. **Independent Development**
- Teams can work on different microfrontends simultaneously
- Different technology stacks can be used for different features
- Independent release cycles

### 2. **Scalability**
- Scale individual microfrontends based on usage
- Better resource utilization
- Horizontal scaling capabilities

### 3. **Maintainability**
- Smaller, focused codebases
- Easier to understand and modify
- Reduced complexity per service

### 4. **Fault Isolation**
- If one microfrontend fails, others continue to work
- Better error boundaries
- Improved overall system reliability

### 5. **Technology Flexibility**
- Use different frameworks for different microfrontends
- Upgrade technologies incrementally
- Experiment with new technologies safely

## Communication Between Microfrontends

### 1. **URL-based Communication**
- Navigation between microfrontends via routing
- Query parameters for passing data

### 2. **Shared State (Future Enhancement)**
- Redux or Zustand for global state
- Event-driven communication
- Shared data services

### 3. **API Communication**
- RESTful APIs for data exchange
- GraphQL for complex data requirements
- WebSocket for real-time updates

## Monitoring and Observability

### 1. **Health Checks**
- Each microfrontend exposes health endpoints
- Docker health checks configured
- Monitoring dashboard integration

### 2. **Logging**
- Centralized logging with structured logs
- Log aggregation and analysis
- Error tracking and alerting

### 3. **Performance Monitoring**
- Application performance monitoring (APM)
- User experience tracking
- Resource utilization monitoring

## Security Considerations

### 1. **Authentication & Authorization**
- Centralized authentication in shell app
- JWT token-based authorization
- Role-based access control

### 2. **Network Security**
- Internal network for microfrontend communication
- HTTPS termination at nginx
- Security headers configuration

### 3. **Data Protection**
- Input validation and sanitization
- XSS and CSRF protection
- Secure data transmission

## Future Enhancements

### 1. **Module Federation**
- Implement Webpack Module Federation
- Runtime sharing of dependencies
- Dynamic microfrontend loading

### 2. **Service Mesh**
- Implement service mesh for better communication
- Traffic management and load balancing
- Enhanced security and observability

### 3. **CI/CD Pipeline**
- Automated testing for each microfrontend
- Independent deployment pipelines
- Blue-green deployments

### 4. **API Gateway**
- Centralized API management
- Rate limiting and throttling
- API versioning and documentation

## Contributing

1. **Development Workflow**
   - Create feature branches for each microfrontend
   - Follow conventional commit messages
   - Write tests for new features
   - Update documentation

2. **Code Standards**
   - Use TypeScript for type safety
   - Follow ESLint and Prettier configurations
   - Maintain consistent coding standards across microfrontends

3. **Testing Strategy**
   - Unit tests for individual components
   - Integration tests for microfrontend interactions
   - End-to-end tests for critical user journeys

## Support

For questions, issues, or contributions, please:
1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Follow the contribution guidelines
4. Reach out to the development team

---

This microfrontends architecture provides a scalable, maintainable, and flexible foundation for the FinFlow application, enabling teams to work independently while delivering a cohesive user experience.