
# GreenCore - Waste Management System

GreenCore is an AI-powered waste management system that helps users classify, dispose of, and track their waste. The system includes features for waste classification, disposal tracking, organization management, and an AI-powered chatbot for waste-related queries.

## Features

- **Waste Classification**: AI-powered image classification for waste types (Recyclable, Biodegradable, Hazardous)
- **Waste Disposal Tracking**: Record and track waste disposal history with photos and weights
- **Organization Management**: Manage waste disposal organizations with ratings and locations
- **AI Chatbot**: Gemini-powered chatbot for waste-related queries and advice
- **User Management**: User registration, authentication, and profile management
- **Dashboard**: Waste statistics and trends visualization
- **FAQs**: Predefined frequently asked questions about waste management

## Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **AI**: Google Gemini
- **Cloud Storage**: Google Cloud Storage
- **Authentication**: JWT
- **Password Hashing**: bcrypt

## API Endpoints

### Users
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user details
- `PUT /api/users/me` - Update user profile
- `POST /api/users/upload-profile-image` - Upload profile image

### Organizations
- `POST /api/orgs` - Create a new organization
- `GET /api/orgs/{org_id}` - Get organization details
- `PUT /api/orgs/{org_id}` - Update organization
- `DELETE /api/orgs/{org_id}` - Delete organization
- `POST /api/orgs/{org_id}/rate` - Rate an organization
- `POST /api/orgs/{org_id}/upload-image` - Upload organization image

### Waste Management
- `POST /api/waste/dispose` - Create a new waste disposal record
- `GET /api/waste/history` - Get user's waste disposal history
- `GET /api/waste/stats` - Get waste statistics
- `GET /api/waste/graph` - Get weekly waste data

### Chat
- `POST /api/chats/start` - Start a new chat session
- `POST /api/chats/continue` - Continue an existing chat session
- `DELETE /api/chats/end/{session_id}` - End a chat session
- `GET /api/chats/user` - Get user's chat history
- `GET /api/chats/{session_id}` - Get chat session details

### FAQs
- `GET /api/faqs` - Get frequently asked questions

## Configuration

The application uses environment variables for configuration. Create a `.env` file with the following variables:

```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=greencore
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GCS_BUCKET_NAME=your-bucket-name
GCS_PROJECT_ID=your-project-id
GCS_PRIVATE_KEY=your-private-key
GCS_CLIENT_EMAIL=your-client-email
GCS_CLIENT_ID=your-client-id
GCS_TOKEN_URI=your-token-uri
GEMINI_API_KEY=your-gemini-api-key
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up environment variables in `.env` file
5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

