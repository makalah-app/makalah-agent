# Agent-Makalah Authentication API Documentation

## Overview

Agent-Makalah provides secure JWT-based authentication with role-based access control, session management, and token blacklisting capabilities. All authentication endpoints are protected by security middleware including rate limiting and comprehensive logging.

## Base URL
```
https://api.agent-makalah.com/api/v1/auth
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant Redis
    participant DB

    Client->>API: POST /register
    API->>DB: Create user
    DB-->>API: User created
    API-->>Client: 201 User registered

    Client->>API: POST /login
    API->>Auth: Validate credentials
    Auth->>DB: Check user
    DB-->>Auth: User valid
    Auth->>Redis: Store session
    Auth-->>API: Generate tokens
    API-->>Client: 200 Access + Refresh tokens

    Client->>API: GET /profile (with Bearer token)
    API->>Auth: Verify token
    Auth->>Redis: Check blacklist
    Auth-->>API: Token valid
    API-->>Client: 200 User profile

    Client->>API: POST /logout
    API->>Auth: Blacklist token
    Auth->>Redis: Add to blacklist
    API-->>Client: 200 Logged out
```

## Endpoints

### 1. User Registration

**POST** `/api/v1/auth/register`

Register a new user account.

#### Request Body
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Request Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address (max 255 chars) |
| password | string | Yes | Password (min 8 chars, must contain uppercase, lowercase, number, special char) |

#### Success Response (201)
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-06-02T13:30:00.000Z",
    "updated_at": "2025-06-02T13:30:00.000Z"
  },
  "message": "User registered successfully"
}
```

#### Error Responses
```json
// 400 - User already exists
{
  "detail": "User with email user@example.com already exists"
}

// 422 - Validation error
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 2. User Login

**POST** `/api/v1/auth/login`

Authenticate user and receive access tokens.

#### Request Body (Form Data)
```
username=user@example.com
password=SecurePassword123!
```

#### Request Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | User email address |
| password | string | Yes | User password |

#### Success Response (200)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false
  },
  "message": "Login successful"
}
```

#### Error Response (401)
```json
{
  "detail": "Incorrect email or password"
}
```

### 3. Token Verification

**GET** `/api/v1/auth/verify`

Verify if the provided token is valid.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Success Response (200)
```json
{
  "valid": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false
  },
  "token_info": {
    "expires_at": "2025-06-02T14:30:00.000Z",
    "issued_at": "2025-06-02T13:30:00.000Z",
    "token_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Error Response (401)
```json
{
  "error": "Token validation failed",
  "message": "Invalid or expired token",
  "status_code": 401
}
```

### 4. Get User Profile

**GET** `/api/v1/auth/profile`

Retrieve current user profile and session information.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Success Response (200)
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-06-02T13:30:00.000Z",
    "updated_at": "2025-06-02T13:30:00.000Z"
  },
  "session_info": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "active_sessions": 1,
    "last_activity": "2025-06-02T13:30:00.000Z"
  },
  "message": "Profile retrieved successfully"
}
```

### 5. Update User Profile

**PUT** `/api/v1/auth/profile`

Update current user profile information.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Request Body
```json
{
  "email": "newemail@example.com"
}
```

#### Success Response (200)
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "newemail@example.com",
    "is_active": true,
    "is_superuser": false,
    "updated_at": "2025-06-02T13:35:00.000Z"
  },
  "message": "Profile updated successfully"
}
```

### 6. Refresh Token

**POST** `/api/v1/auth/refresh`

Generate new access token using refresh token.

#### Request Body
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Success Response (200)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "message": "Token refreshed successfully"
}
```

#### Error Response (401)
```json
{
  "detail": "Invalid or expired refresh token"
}
```

### 7. User Logout

**POST** `/api/v1/auth/logout`

Logout user and blacklist current token.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Success Response (200)
```json
{
  "status": "success",
  "message": "Successfully logged out"
}
```

### 8. Logout All Sessions

**POST** `/api/v1/auth/logout-all`

Logout user from all active sessions.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Success Response (200)
```json
{
  "status": "success",
  "message": "Successfully logged out from all sessions",
  "sessions_terminated": 3
}
```

## Authentication Headers

All protected endpoints require the Authorization header:

```
Authorization: Bearer <access_token>
```

## Rate Limiting

Authentication endpoints have strict rate limiting:

- **Login endpoint**: 5 attempts per 5 minutes per IP
- **Registration**: 3 attempts per 10 minutes per IP  
- **General auth endpoints**: 100 requests per minute per IP

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 4
X-RateLimit-Reset: 300
```

## Security Features

### 1. JWT Token Structure
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_superuser": false,
  "token_id": "550e8400-e29b-41d4-a716-446655440000",
  "iat": 1735738200,
  "exp": 1735741800
}
```

### 2. Token Blacklisting
- Tokens are blacklisted on logout
- Refresh operations blacklist old tokens
- Mass logout blacklists all user tokens
- Blacklisted tokens stored in Redis with TTL

### 3. Session Management
- Each login creates a unique session
- Session tracking in Redis
- Configurable session limits per user
- Session cleanup on logout

### 4. Security Middleware
- **Security Headers**: CSP, XSS protection, frame options
- **Rate Limiting**: Endpoint-specific limits
- **Request Logging**: Security event monitoring
- **CORS**: Configurable origins

## Error Handling

All endpoints follow consistent error response format:

```json
{
  "error": "Error type",
  "message": "Human readable message", 
  "status_code": 400,
  "timestamp": "2025-06-02T13:30:00.000Z"
}
```

## Common HTTP Status Codes

| Status | Description |
|--------|-------------|
| 200 | Success |
| 201 | Created (registration) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid credentials/token) |
| 403 | Forbidden (insufficient permissions) |
| 422 | Unprocessable Entity (validation error) |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |

## Examples

### Complete Authentication Flow

```bash
# 1. Register new user
curl -X POST "https://api.agent-makalah.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'

# 2. Login and get tokens
curl -X POST "https://api.agent-makalah.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=SecurePassword123!'

# 3. Use access token to get profile
curl -X GET "https://api.agent-makalah.com/api/v1/auth/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 4. Refresh token when needed
curl -X POST "https://api.agent-makalah.com/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'

# 5. Logout
curl -X POST "https://api.agent-makalah.com/api/v1/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### JavaScript/TypeScript Client Example

```typescript
class AgentMakalahAuth {
  private baseUrl = 'https://api.agent-makalah.com/api/v1/auth';
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  async register(email: string, password: string) {
    const response = await fetch(`${this.baseUrl}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      throw new Error('Registration failed');
    }
    
    return response.json();
  }

  async login(email: string, password: string) {
    const response = await fetch(`${this.baseUrl}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password })
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;
    
    return data;
  }

  async getProfile() {
    const response = await fetch(`${this.baseUrl}/profile`, {
      headers: { 'Authorization': `Bearer ${this.accessToken}` }
    });
    
    if (!response.ok) {
      throw new Error('Failed to get profile');
    }
    
    return response.json();
  }

  async logout() {
    const response = await fetch(`${this.baseUrl}/logout`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${this.accessToken}` }
    });
    
    this.accessToken = null;
    this.refreshToken = null;
    
    return response.json();
  }
}
```

### Python Client Example

```python
import requests
import json

class AgentMakalahAuth:
    def __init__(self, base_url="https://api.agent-makalah.com/api/v1/auth"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def register(self, email, password):
        response = requests.post(
            f"{self.base_url}/register",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email, password):
        response = requests.post(
            f"{self.base_url}/login",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        
        return data
    
    def get_profile(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/profile", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def logout(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(f"{self.base_url}/logout", headers=headers)
        
        self.access_token = None
        self.refresh_token = None
        
        return response.json()
```

## Testing

### Running Authentication Tests

```bash
# Run comprehensive test suite
python tests/auth/test_authentication_endpoints.py

# Run simple authentication test
python test_auth_simple.py

# Run middleware security tests
python tests/middleware/test_security_middleware.py
```

### Test Coverage

The authentication system has comprehensive test coverage including:

- ✅ User registration validation
- ✅ Login with valid/invalid credentials  
- ✅ Token verification and expiration
- ✅ Profile management (get/update)
- ✅ Token refresh workflow
- ✅ Logout and session management
- ✅ Rate limiting enforcement
- ✅ Security middleware integration
- ✅ Error handling and edge cases

## Security Considerations

1. **Password Security**: Bcrypt hashing with configurable rounds
2. **Token Security**: Short-lived access tokens, longer refresh tokens
3. **Rate Limiting**: Prevents brute force attacks
4. **Session Management**: Prevents session hijacking
5. **CORS Policy**: Restricts cross-origin requests
6. **Security Headers**: Comprehensive XSS/CSRF protection
7. **Input Validation**: Pydantic models for all inputs
8. **Audit Logging**: All authentication events logged

## Configuration

Key authentication settings can be configured via environment variables:

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis Configuration (for sessions/blacklist)
UPSTASH_REDIS_REST_URL=your-redis-url
UPSTASH_REDIS_REST_TOKEN=your-redis-token

# Security Configuration
BCRYPT_ROUNDS=12
MAX_LOGIN_ATTEMPTS=5
RATE_LIMIT_WINDOW=300
``` 