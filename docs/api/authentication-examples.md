# Agent-Makalah Authentication Examples

This document provides practical examples and implementation guides for integrating with the Agent-Makalah authentication system.

## Quick Start Guide

### 1. Basic Setup

First, ensure you have the base URL and understand the authentication flow:

```bash
export API_BASE_URL="https://api.agent-makalah.com"
export AUTH_ENDPOINT="/api/v1/auth"
```

### 2. Complete Authentication Flow

```bash
#!/bin/bash
# complete-auth-flow.sh

BASE_URL="https://api.agent-makalah.com/api/v1/auth"

# 1. Register a new user
echo "🔐 Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@agent-makalah.com",
    "password": "DemoPassword123!"
  }')

echo "Registration Response: $REGISTER_RESPONSE"

# 2. Login and get tokens
echo "🔑 Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=demo@agent-makalah.com&password=DemoPassword123!')

echo "Login Response: $LOGIN_RESPONSE"

# Extract access token
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['refresh_token'])")

echo "Access Token: $ACCESS_TOKEN"

# 3. Get user profile
echo "👤 Getting user profile..."
PROFILE_RESPONSE=$(curl -s -X GET "$BASE_URL/profile" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Profile Response: $PROFILE_RESPONSE"

# 4. Update profile
echo "✏️ Updating profile..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/profile" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated-demo@agent-makalah.com"
  }')

echo "Update Response: $UPDATE_RESPONSE"

# 5. Refresh token
echo "🔄 Refreshing token..."
REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}")

echo "Refresh Response: $REFRESH_RESPONSE"

# Extract new access token
NEW_ACCESS_TOKEN=$(echo $REFRESH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 6. Logout
echo "🚪 Logging out..."
LOGOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/logout" \
  -H "Authorization: Bearer $NEW_ACCESS_TOKEN")

echo "Logout Response: $LOGOUT_RESPONSE"
echo "✅ Complete authentication flow finished!"
```

## Language-Specific Examples

### Python Implementation

```python
"""
Agent-Makalah Python Authentication Client
Production-ready implementation with error handling and token management
"""

import requests
import json
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TokenInfo:
    """Token information container"""
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def is_expired(self) -> bool:
        """Check if access token is expired (with 5 minute buffer)"""
        if not self.created_at:
            return True
        
        expiry_time = self.created_at + timedelta(seconds=self.expires_in - 300)  # 5 min buffer
        return datetime.now() > expiry_time


class AgentMakalahAuthError(Exception):
    """Custom authentication error"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class AgentMakalahAuth:
    """
    Production-ready Agent-Makalah authentication client
    
    Features:
    - Automatic token refresh
    - Error handling and retries
    - Session management
    - Rate limit handling
    """
    
    def __init__(self, base_url: str = "https://api.agent-makalah.com/api/v1/auth"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token_info: Optional[TokenInfo] = None
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'AgentMakalah-Python-Client/1.0.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise AgentMakalahAuthError(
                    f"Rate limited. Retry after {retry_after} seconds",
                    status_code=429,
                    response_data=response.json() if response.content else None
                )
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise AgentMakalahAuthError(f"Request failed: {str(e)}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and extract data"""
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise AgentMakalahAuthError(
                f"Invalid JSON response (status: {response.status_code})",
                status_code=response.status_code
            )
        
        if not response.ok:
            error_message = data.get('detail', data.get('message', f'HTTP {response.status_code}'))
            raise AgentMakalahAuthError(
                error_message,
                status_code=response.status_code,
                response_data=data
            )
        
        return data
    
    def register(self, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User email address
            password: User password (min 8 chars, complex)
            
        Returns:
            User registration data
            
        Raises:
            AgentMakalahAuthError: If registration fails
        """
        response = self._make_request(
            'POST', '/register',
            json={'email': email, 'password': password}
        )
        
        return self._handle_response(response)
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user and store tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Login response with tokens and user info
        """
        response = self._make_request(
            'POST', '/login',
            data={'username': email, 'password': password},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        data = self._handle_response(response)
        
        # Store token information
        self.token_info = TokenInfo(
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expires_in=data['expires_in'],
            token_type=data['token_type']
        )
        
        # Update session headers
        self.session.headers['Authorization'] = f"Bearer {self.token_info.access_token}"
        
        return data
    
    def refresh_token(self) -> Dict[str, Any]:
        """
        Refresh access token using refresh token
        
        Returns:
            New token information
        """
        if not self.token_info or not self.token_info.refresh_token:
            raise AgentMakalahAuthError("No refresh token available")
        
        response = self._make_request(
            'POST', '/refresh',
            json={'refresh_token': self.token_info.refresh_token}
        )
        
        data = self._handle_response(response)
        
        # Update token information
        self.token_info = TokenInfo(
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expires_in=data['expires_in'],
            token_type=data['token_type']
        )
        
        # Update session headers
        self.session.headers['Authorization'] = f"Bearer {self.token_info.access_token}"
        
        return data
    
    def _ensure_valid_token(self):
        """Ensure we have a valid access token, refresh if needed"""
        if not self.token_info:
            raise AgentMakalahAuthError("Not authenticated. Please login first.")
        
        if self.token_info.is_expired:
            try:
                self.refresh_token()
            except AgentMakalahAuthError as e:
                if e.status_code == 401:
                    # Refresh token is also expired, need to login again
                    self.token_info = None
                    self.session.headers.pop('Authorization', None)
                    raise AgentMakalahAuthError("Session expired. Please login again.")
                raise
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get current user profile
        
        Returns:
            User profile data
        """
        self._ensure_valid_token()
        
        response = self._make_request('GET', '/profile')
        return self._handle_response(response)
    
    def update_profile(self, **updates) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            **updates: Fields to update (e.g., email="new@email.com")
            
        Returns:
            Updated user profile data
        """
        self._ensure_valid_token()
        
        response = self._make_request(
            'PUT', '/profile',
            json=updates
        )
        
        return self._handle_response(response)
    
    def verify_token(self) -> Dict[str, Any]:
        """
        Verify current token validity
        
        Returns:
            Token verification data
        """
        self._ensure_valid_token()
        
        response = self._make_request('GET', '/verify')
        return self._handle_response(response)
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout current session
        
        Returns:
            Logout confirmation
        """
        if not self.token_info:
            raise AgentMakalahAuthError("Not authenticated")
        
        response = self._make_request('POST', '/logout')
        data = self._handle_response(response)
        
        # Clear stored tokens
        self.token_info = None
        self.session.headers.pop('Authorization', None)
        
        return data
    
    def logout_all_sessions(self) -> Dict[str, Any]:
        """
        Logout from all sessions
        
        Returns:
            Logout confirmation with session count
        """
        self._ensure_valid_token()
        
        response = self._make_request('POST', '/logout-all')
        data = self._handle_response(response)
        
        # Clear stored tokens
        self.token_info = None
        self.session.headers.pop('Authorization', None)
        
        return data
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return self.token_info is not None and not self.token_info.is_expired


# Usage examples
def main():
    """Example usage of the authentication client"""
    
    # Initialize client
    auth = AgentMakalahAuth()
    
    try:
        # Register new user
        print("🔐 Registering user...")
        register_result = auth.register(
            email="demo-python@agent-makalah.com",
            password="PythonDemo123!"
        )
        print(f"✅ Registration successful: {register_result['message']}")
        
        # Login
        print("🔑 Logging in...")
        login_result = auth.login(
            email="demo-python@agent-makalah.com",
            password="PythonDemo123!"
        )
        print(f"✅ Login successful: {login_result['message']}")
        print(f"📝 Session ID: {login_result['session_id']}")
        
        # Get profile
        print("👤 Getting profile...")
        profile = auth.get_profile()
        print(f"✅ Profile: {profile['user']['email']}")
        print(f"📊 Active sessions: {profile['session_info']['active_sessions']}")
        
        # Update profile
        print("✏️ Updating profile...")
        updated_profile = auth.update_profile(
            email="updated-python-demo@agent-makalah.com"
        )
        print(f"✅ Profile updated: {updated_profile['user']['email']}")
        
        # Verify token
        print("🔍 Verifying token...")
        token_info = auth.verify_token()
        print(f"✅ Token valid: {token_info['valid']}")
        
        # Test automatic token refresh (simulate expiry)
        print("🔄 Testing token refresh...")
        if auth.token_info:
            # Force token to appear expired for testing
            auth.token_info.created_at = datetime.now() - timedelta(hours=2)
            
            # This should automatically refresh the token
            profile = auth.get_profile()
            print("✅ Token automatically refreshed")
        
        # Logout
        print("🚪 Logging out...")
        logout_result = auth.logout()
        print(f"✅ Logout successful: {logout_result['message']}")
        
    except AgentMakalahAuthError as e:
        print(f"❌ Authentication error: {e.message}")
        if e.status_code:
            print(f"   Status code: {e.status_code}")
        if e.response_data:
            print(f"   Response: {e.response_data}")
    
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
```

### JavaScript/TypeScript Implementation

```typescript
/**
 * Agent-Makalah TypeScript Authentication Client
 * Production-ready implementation with automatic token management
 */

interface TokenInfo {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  created_at: Date;
}

interface UserProfile {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

interface SessionInfo {
  session_id: string;
  active_sessions: number;
  last_activity: string;
}

interface ApiError {
  error?: string;
  detail?: string;
  message?: string;
  status_code?: number;
}

class AgentMakalahAuthError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public responseData?: ApiError
  ) {
    super(message);
    this.name = 'AgentMakalahAuthError';
  }
}

class AgentMakalahAuth {
  private baseUrl: string;
  private tokenInfo: TokenInfo | null = null;
  private refreshPromise: Promise<TokenInfo> | null = null;

  constructor(baseUrl: string = 'https://api.agent-makalah.com/api/v1/auth') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async makeRequest<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'User-Agent': 'AgentMakalah-JS-Client/1.0.0',
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers: defaultHeaders,
      });

      let data: any;
      try {
        data = await response.json();
      } catch {
        throw new AgentMakalahAuthError(
          `Invalid JSON response (status: ${response.status})`,
          response.status
        );
      }

      if (!response.ok) {
        const errorMessage = data.detail || data.message || `HTTP ${response.status}`;
        throw new AgentMakalahAuthError(errorMessage, response.status, data);
      }

      return data;
    } catch (error) {
      if (error instanceof AgentMakalahAuthError) {
        throw error;
      }
      throw new AgentMakalahAuthError(`Request failed: ${error.message}`);
    }
  }

  private isTokenExpired(): boolean {
    if (!this.tokenInfo) return true;
    
    const expiryTime = new Date(
      this.tokenInfo.created_at.getTime() + 
      (this.tokenInfo.expires_in - 300) * 1000 // 5 min buffer
    );
    
    return new Date() > expiryTime;
  }

  private async ensureValidToken(): Promise<void> {
    if (!this.tokenInfo) {
      throw new AgentMakalahAuthError('Not authenticated. Please login first.');
    }

    if (this.isTokenExpired()) {
      // Prevent multiple simultaneous refresh requests
      if (!this.refreshPromise) {
        this.refreshPromise = this.refreshToken();
      }
      
      try {
        await this.refreshPromise;
      } catch (error) {
        if (error instanceof AgentMakalahAuthError && error.statusCode === 401) {
          // Refresh token expired, need to login again
          this.tokenInfo = null;
          throw new AgentMakalahAuthError('Session expired. Please login again.');
        }
        throw error;
      } finally {
        this.refreshPromise = null;
      }
    }
  }

  async register(email: string, password: string): Promise<any> {
    return this.makeRequest('/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async login(email: string, password: string): Promise<any> {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await this.makeRequest('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    // Store token information
    this.tokenInfo = {
      access_token: response.access_token,
      refresh_token: response.refresh_token,
      token_type: response.token_type,
      expires_in: response.expires_in,
      created_at: new Date(),
    };

    return response;
  }

  async refreshToken(): Promise<TokenInfo> {
    if (!this.tokenInfo?.refresh_token) {
      throw new AgentMakalahAuthError('No refresh token available');
    }

    const response = await this.makeRequest('/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: this.tokenInfo.refresh_token }),
    });

    // Update token information
    this.tokenInfo = {
      access_token: response.access_token,
      refresh_token: response.refresh_token,
      token_type: response.token_type,
      expires_in: response.expires_in,
      created_at: new Date(),
    };

    return this.tokenInfo;
  }

  async getProfile(): Promise<{ user: UserProfile; session_info: SessionInfo }> {
    await this.ensureValidToken();
    
    return this.makeRequest('/profile', {
      headers: {
        Authorization: `Bearer ${this.tokenInfo!.access_token}`,
      },
    });
  }

  async updateProfile(updates: Partial<Pick<UserProfile, 'email'>>): Promise<any> {
    await this.ensureValidToken();
    
    return this.makeRequest('/profile', {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${this.tokenInfo!.access_token}`,
      },
      body: JSON.stringify(updates),
    });
  }

  async verifyToken(): Promise<any> {
    await this.ensureValidToken();
    
    return this.makeRequest('/verify', {
      headers: {
        Authorization: `Bearer ${this.tokenInfo!.access_token}`,
      },
    });
  }

  async logout(): Promise<any> {
    if (!this.tokenInfo) {
      throw new AgentMakalahAuthError('Not authenticated');
    }

    const response = await this.makeRequest('/logout', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.tokenInfo.access_token}`,
      },
    });

    // Clear stored tokens
    this.tokenInfo = null;
    
    return response;
  }

  async logoutAllSessions(): Promise<any> {
    await this.ensureValidToken();
    
    const response = await this.makeRequest('/logout-all', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.tokenInfo!.access_token}`,
      },
    });

    // Clear stored tokens
    this.tokenInfo = null;
    
    return response;
  }

  get isAuthenticated(): boolean {
    return this.tokenInfo !== null && !this.isTokenExpired();
  }

  get currentUser(): UserProfile | null {
    return this.tokenInfo ? null : null; // Would need to be stored from login response
  }
}

// Usage example
async function example() {
  const auth = new AgentMakalahAuth();

  try {
    // Register
    console.log('🔐 Registering user...');
    await auth.register('demo-ts@agent-makalah.com', 'TypeScriptDemo123!');
    console.log('✅ Registration successful');

    // Login
    console.log('🔑 Logging in...');
    const loginResult = await auth.login('demo-ts@agent-makalah.com', 'TypeScriptDemo123!');
    console.log('✅ Login successful:', loginResult.message);

    // Get profile
    console.log('👤 Getting profile...');
    const profile = await auth.getProfile();
    console.log('✅ Profile:', profile.user.email);

    // Update profile
    console.log('✏️ Updating profile...');
    await auth.updateProfile({ email: 'updated-ts-demo@agent-makalah.com' });
    console.log('✅ Profile updated');

    // Logout
    console.log('🚪 Logging out...');
    await auth.logout();
    console.log('✅ Logout successful');

  } catch (error) {
    if (error instanceof AgentMakalahAuthError) {
      console.error('❌ Auth error:', error.message);
      if (error.statusCode) console.error('   Status:', error.statusCode);
    } else {
      console.error('💥 Unexpected error:', error);
    }
  }
}

// React Hook Example
function useAgentMakalahAuth() {
  const [auth] = useState(() => new AgentMakalahAuth());
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await auth.login(email, password);
      const profile = await auth.getProfile();
      setUser(profile.user);
      return result;
    } catch (err) {
      const errorMessage = err instanceof AgentMakalahAuthError ? err.message : 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    
    try {
      await auth.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setLoading(false);
    }
  };

  return {
    auth,
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: auth.isAuthenticated,
  };
}

export { AgentMakalahAuth, AgentMakalahAuthError, type UserProfile, type SessionInfo };
```

## Integration Patterns

### 1. Express.js Middleware

```javascript
const AgentMakalahAuth = require('./agent-makalah-auth');

function createAuthMiddleware(options = {}) {
  const auth = new AgentMakalahAuth(options.baseUrl);
  
  return async (req, res, next) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    try {
      // Verify token with Agent-Makalah API
      const verification = await auth.verifyToken(token);
      req.user = verification.user;
      next();
    } catch (error) {
      res.status(401).json({ error: 'Invalid token' });
    }
  };
}

// Usage
app.use('/api/protected', createAuthMiddleware());
```

### 2. React Authentication Context

```tsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AgentMakalahAuth, UserProfile } from './agent-makalah-auth';

interface AuthState {
  user: UserProfile | null;
  loading: boolean;
  error: string | null;
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

type AuthAction = 
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; user: UserProfile }
  | { type: 'AUTH_ERROR'; error: string }
  | { type: 'AUTH_LOGOUT' };

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, loading: true, error: null };
    case 'AUTH_SUCCESS':
      return { ...state, loading: false, user: action.user, error: null };
    case 'AUTH_ERROR':
      return { ...state, loading: false, error: action.error };
    case 'AUTH_LOGOUT':
      return { ...state, user: null, loading: false, error: null };
    default:
      return state;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    loading: false,
    error: null
  });

  const auth = new AgentMakalahAuth();

  const login = async (email: string, password: string) => {
    dispatch({ type: 'AUTH_START' });
    
    try {
      await auth.login(email, password);
      const profile = await auth.getProfile();
      dispatch({ type: 'AUTH_SUCCESS', user: profile.user });
    } catch (error) {
      dispatch({ type: 'AUTH_ERROR', error: error.message });
      throw error;
    }
  };

  const logout = async () => {
    try {
      await auth.logout();
      dispatch({ type: 'AUTH_LOGOUT' });
    } catch (error) {
      console.error('Logout error:', error);
      dispatch({ type: 'AUTH_LOGOUT' }); // Logout locally anyway
    }
  };

  const register = async (email: string, password: string) => {
    dispatch({ type: 'AUTH_START' });
    
    try {
      await auth.register(email, password);
      await login(email, password); // Auto-login after registration
    } catch (error) {
      dispatch({ type: 'AUTH_ERROR', error: error.message });
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

## Testing Examples

### Unit Testing with Jest

```javascript
// agent-makalah-auth.test.js
import { AgentMakalahAuth, AgentMakalahAuthError } from './agent-makalah-auth';

// Mock fetch
global.fetch = jest.fn();

describe('AgentMakalahAuth', () => {
  let auth;

  beforeEach(() => {
    auth = new AgentMakalahAuth('https://test-api.agent-makalah.com/api/v1/auth');
    fetch.mockClear();
  });

  describe('register', () => {
    it('should register user successfully', async () => {
      const mockResponse = {
        user: { id: '123', email: 'test@example.com' },
        message: 'User registered successfully'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await auth.register('test@example.com', 'password123');
      
      expect(fetch).toHaveBeenCalledWith(
        'https://test-api.agent-makalah.com/api/v1/auth/register',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
        })
      );
      
      expect(result).toEqual(mockResponse);
    });

    it('should throw error for duplicate email', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: () => Promise.resolve({ detail: 'User already exists' })
      });

      await expect(auth.register('existing@example.com', 'password123'))
        .rejects
        .toThrow(AgentMakalahAuthError);
    });
  });

  describe('login', () => {
    it('should login and store tokens', async () => {
      const mockResponse = {
        access_token: 'access_token_123',
        refresh_token: 'refresh_token_123',
        token_type: 'bearer',
        expires_in: 3600,
        user: { id: '123', email: 'test@example.com' }
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });

      const result = await auth.login('test@example.com', 'password123');
      
      expect(auth.tokenInfo).toBeTruthy();
      expect(auth.tokenInfo.access_token).toBe('access_token_123');
      expect(auth.isAuthenticated).toBe(true);
    });
  });

  describe('token refresh', () => {
    beforeEach(() => {
      // Set up authenticated state
      auth.tokenInfo = {
        access_token: 'old_token',
        refresh_token: 'refresh_token',
        expires_in: 3600,
        token_type: 'bearer',
        created_at: new Date(Date.now() - 7200000) // 2 hours ago (expired)
      };
    });

    it('should automatically refresh expired token', async () => {
      const mockRefreshResponse = {
        access_token: 'new_access_token',
        refresh_token: 'new_refresh_token',
        expires_in: 3600,
        token_type: 'bearer'
      };

      const mockProfileResponse = {
        user: { id: '123', email: 'test@example.com' }
      };

      fetch
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockRefreshResponse)
        })
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockProfileResponse)
        });

      const profile = await auth.getProfile();
      
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/refresh'),
        expect.objectContaining({ method: 'POST' })
      );
      
      expect(auth.tokenInfo.access_token).toBe('new_access_token');
    });
  });
});
```

## Security Best Practices

### 1. Token Storage (Browser)

```javascript
// Secure token storage utility
class SecureTokenStorage {
  static setTokens(tokenInfo) {
    // Store refresh token in httpOnly cookie (server-side only)
    // Store access token in memory only (most secure for SPA)
    
    // For demonstration, using sessionStorage (better than localStorage)
    sessionStorage.setItem('agent_makalah_access_token', tokenInfo.access_token);
    
    // In production, refresh token should be httpOnly cookie
    document.cookie = `agent_makalah_refresh_token=${tokenInfo.refresh_token}; HttpOnly; Secure; SameSite=Strict; Path=/`;
  }
  
  static getAccessToken() {
    return sessionStorage.getItem('agent_makalah_access_token');
  }
  
  static clearTokens() {
    sessionStorage.removeItem('agent_makalah_access_token');
    document.cookie = 'agent_makalah_refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }
}
```

### 2. CSRF Protection

```javascript
// CSRF token handling
class CSRFProtection {
  static async getCSRFToken() {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
  }
  
  static addCSRFHeader(headers = {}) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (csrfToken) {
      headers['X-CSRF-Token'] = csrfToken;
    }
    return headers;
  }
}
```

### 3. Request Interceptors

```javascript
// Axios interceptor example
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://api.agent-makalah.com',
});

// Request interceptor to add auth header
apiClient.interceptors.request.use((config) => {
  const token = SecureTokenStorage.getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      
      try {
        await auth.refreshToken();
        error.config.headers.Authorization = `Bearer ${auth.tokenInfo.access_token}`;
        return apiClient.request(error.config);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

## Troubleshooting

### Common Issues

1. **Token Refresh Loops**
   ```javascript
   // Prevent infinite refresh loops
   let refreshPromise = null;
   
   async function refreshToken() {
     if (refreshPromise) {
       return refreshPromise;
     }
     
     refreshPromise = actualRefreshFunction();
     
     try {
       const result = await refreshPromise;
       return result;
     } finally {
       refreshPromise = null;
     }
   }
   ```

2. **Rate Limiting Handling**
   ```javascript
   async function handleRateLimit(response) {
     if (response.status === 429) {
       const retryAfter = response.headers.get('Retry-After');
       await new Promise(resolve => 
         setTimeout(resolve, (retryAfter || 60) * 1000)
       );
       // Retry the request
     }
   }
   ```

3. **Network Error Recovery**
   ```javascript
   async function retryRequest(fn, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await fn();
       } catch (error) {
         if (i === maxRetries - 1 || error.statusCode < 500) {
           throw error;
         }
         await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
       }
     }
   }
   ```

## Performance Optimization

### Token Prefetching

```javascript
class OptimizedAuth extends AgentMakalahAuth {
  constructor(options) {
    super(options);
    this.setupTokenRefreshTimer();
  }
  
  setupTokenRefreshTimer() {
    setInterval(() => {
      if (this.tokenInfo && this.shouldRefreshSoon()) {
        this.refreshToken().catch(console.error);
      }
    }, 60000); // Check every minute
  }
  
  shouldRefreshSoon() {
    if (!this.tokenInfo) return false;
    
    const refreshTime = new Date(
      this.tokenInfo.created_at.getTime() + 
      (this.tokenInfo.expires_in - 600) * 1000 // Refresh 10 minutes early
    );
    
    return new Date() > refreshTime;
  }
}
```

This comprehensive guide covers all aspects of integrating with the Agent-Makalah authentication system, from basic usage to production-ready implementations with proper error handling, security measures, and performance optimizations. 