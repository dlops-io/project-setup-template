# Frontend React

React-based frontend application for the MLOps project.

## Purpose

This service provides:
- User interface for interacting with ML models
- Data visualization and exploration
- Model prediction interface
- RAG query interface
- Admin dashboard for model management

## Getting Started

### Prerequisites
- Node.js 20+
- npm or yarn

### Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local`:
```bash
REACT_APP_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm start
```

4. Access the app:
http://localhost:3000

## Implementation Tasks

Students should implement:

1. **Pages/Views**
   - Home/Landing page
   - Data upload/collection interface
   - Model prediction interface
   - RAG query interface
   - Model management dashboard

2. **Components**
   - File upload component
   - Prediction form
   - Results visualization
   - Loading states
   - Error handling

3. **State Management**
   - API integration with backend
   - Global state (Context API or Redux)
   - Form state management

4. **Styling**
   - Responsive design
   - UI component library (Material-UI, Chakra, etc.)
   - Dark/light mode

## Project Structure

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/      # Reusable components
│   ├── pages/          # Page components
│   ├── services/       # API clients
│   ├── hooks/          # Custom React hooks
│   ├── context/        # Context providers
│   ├── utils/          # Utility functions
│   ├── App.js
│   └── index.js
├── package.json
└── Dockerfile
```

## Available Scripts

### Development
```bash
npm start         # Start dev server
npm test          # Run tests
npm run build     # Build for production
npm run lint      # Run linter
```

## API Integration

Connect to backend API:

```javascript
const API_URL = process.env.REACT_APP_API_URL;

async function predict(features) {
  const response = await fetch(`${API_URL}/api/v1/model/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ features })
  });
  return response.json();
}
```

## Docker

Build:
```bash
docker build -t mlops-frontend-react .
```

Run:
```bash
docker run -p 3000:80 mlops-frontend-react
```

## Deployment

The frontend is built as a static site and served through:
- **Development**: React dev server
- **Production**: Nginx in Docker container → deployed to GKE

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENV`: Environment (development/production)

## Recommended Libraries

- **UI Framework**: Material-UI, Chakra UI, or Ant Design
- **State Management**: React Context API or Redux Toolkit
- **HTTP Client**: Axios or Fetch API
- **Routing**: React Router
- **Charts**: Recharts or Chart.js
- **Forms**: React Hook Form
