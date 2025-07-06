# AgentLogger API Usage Examples

## 🔧 Practical API Examples: Frontend ↔ Backend Communication

This document provides real-world examples of how the frontend and backend communicate through the API.

## 🔐 Authentication Examples

### 1. User Registration

**Frontend (React)**
```typescript
// From: frontend/src/pages/SignIn.tsx
const handleRegister = async (formData: { email: string; password: string; full_name: string }) => {
  try {
    const response = await register({
      email: formData.email,
      password: formData.password,
      full_name: formData.full_name
    });
    
    // Automatically log in after registration
    await login({ email: formData.email, password: formData.password });
    
    toast.success("Registration successful!");
    navigate("/dashboard");
  } catch (error) {
    toast.error(error.message);
  }
};
```

**API Client (lib/api.ts)**
```typescript
export const register = async (userData: UserCreate): Promise<User> => {
  return await apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify(userData),
  });
};
```

**Backend (FastAPI)**
```python
# From: app/api/v1/endpoints/auth.py
@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(
        id=str(uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
```

**HTTP Request/Response Flow**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. User Login

**Frontend → Backend Flow**
```typescript
// Frontend call
const loginData = { email: "user@example.com", password: "password123" };
const response = await login(loginData);

// API Client function
export const login = async (credentials: UserLogin): Promise<AuthResponse> => {
  return await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
};
```

**Backend Response**
```python
@router.post("/login", response_model=dict)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Validate credentials
    user = get_user_by_email(db, user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate JWT token
    token_data = {"user_id": str(user.id), "email": user.email}
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
```

**HTTP Flow**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true
  }
}
```

## 🧪 Code Analysis Examples

### 1. Quick Code Analysis

**Frontend (Playground)**
```typescript
// From: frontend/src/pages/Playground.tsx
const handleAnalyze = async () => {
  const request: AnalysisRequestCreate = {
    code: "print(hello world)",  // Intentional syntax error
    language: "python",
    traceback: "SyntaxError: invalid syntax"
  };
  
  try {
    const result = await quickAnalyzeCode(request);
    setAnalysisResult(result);
    toast.success("Analysis complete!");
  } catch (error) {
    toast.error(`Analysis failed: ${error.message}`);
  }
};
```

**API Client**
```typescript
export const quickAnalyzeCode = async (data: AnalysisRequestCreate): Promise<AnalysisResult> => {
  return await apiRequest("/analyze/quick", {
    method: "POST",
    body: JSON.stringify(data),
  }, true); // Use JWT auth
};
```

**Backend Processing**
```python
# From: app/api/v1/endpoints/analyze.py
@router.post("/quick", response_model=AnalysisResult)
async def quick_analyze(
    analysis_data: AnalysisRequestCreate,
    request: Request,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    # Get user from JWT token
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Perform analysis
    result = await analyze_code(db, analysis_data, user_id, agent_system)
    return result
```

**HTTP Request/Response**
```http
POST /api/v1/analyze/quick
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "code": "print(hello world)",
  "language": "python",
  "traceback": "SyntaxError: invalid syntax"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "request_id": "analysis-uuid-here",
  "status": "completed",
  "issues": [
    {
      "type": "syntax_error",
      "severity": "high",
      "message": "Missing quotes around string literal",
      "line_start": 1,
      "code_snippet": "print(hello world)"
    }
  ]
}
```

### 2. Code Fix Generation

**Frontend Request**
```typescript
// From: frontend/src/pages/Playground.tsx
const handleGenerateFix = async () => {
  const request: FixRequestCreate = {
    code: "print(hello world)",
    language: "python",
    error_message: "SyntaxError: invalid syntax",
    context: "Generated from Playground"
  };
  
  const result = await createFix(request);
  setFixResult(result);
};
```

**Backend Processing**
```python
# From: app/api/v1/endpoints/fix.py
@router.post("/", response_model=FixRequestResponse)
async def create_fix(
    fix_request: FixRequestCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    agent_system: AgentSystem = Depends(get_agent_system_dependency),
):
    user_id = getattr(request.state, 'user_id', None)
    
    # Create fix request in database
    db_fix_request = FixRequest(
        user_id=user_id,
        code=fix_request.code,
        language=fix_request.language,
        error_message=fix_request.error_message,
        status=FixStatus.PENDING
    )
    
    db.add(db_fix_request)
    db.commit()
    
    # Process fix in background
    background_tasks.add_task(process_fix_background, db, str(db_fix_request.id), agent_system)
    
    return FixRequestResponse.model_validate(db_fix_request)
```

**HTTP Flow**
```http
POST /api/v1/fix
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "code": "print(hello world)",
  "language": "python",
  "error_message": "SyntaxError: invalid syntax",
  "context": "Generated from Playground"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "fix-uuid-here",
  "status": "pending",
  "code": "print(hello world)",
  "language": "python",
  "error_message": "SyntaxError: invalid syntax",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🔑 API Key Management Examples

### 1. Create API Key

**Frontend (API Keys Page)**
```typescript
// From: frontend/src/pages/ApiKeys.tsx
const handleCreateKey = async () => {
  try {
    const result = await createApiKey(keyName);
    setApiKeys(prev => [...prev, result]);
    setShowCreateForm(false);
    setKeyName("");
    
    // Show the key once (security measure)
    toast.success("API key created successfully!");
  } catch (error) {
    toast.error(`Failed to create API key: ${error.message}`);
  }
};
```

**API Client**
```typescript
export const createApiKey = async (name: string): Promise<ApiKeyCreateResponse> => {
  return await apiRequest("/api-keys", {
    method: "POST",
    body: JSON.stringify({ name }),
  }, true);
};
```

**Backend Processing**
```python
# From: app/api/v1/endpoints/api_keys.py
@router.post("/", response_model=ApiKeyCreateResponse)
async def create_new_api_key(
    api_key_data: ApiKeyCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = getattr(request.state, 'user_id', None)
    
    # Generate new API key
    from app.services.api_key_service import create_api_key
    
    result = create_api_key(db, api_key_data, user_id)
    return result
```

**HTTP Flow**
```http
POST /api/v1/api-keys
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "My Development Key"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "al_1234567890abcdef...",
  "id": "key-uuid-here",
  "name": "My Development Key",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. List API Keys

**Frontend**
```typescript
// From: frontend/src/pages/ApiKeys.tsx
useEffect(() => {
  const fetchApiKeys = async () => {
    try {
      const keys = await getApiKeys();
      setApiKeys(keys);
    } catch (error) {
      toast.error("Failed to load API keys");
    }
  };
  
  fetchApiKeys();
}, []);
```

**Backend Response**
```python
@router.get("/", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = getattr(request.state, 'user_id', None)
    return get_api_keys_by_user(db, user_id)
```

**HTTP Flow**
```http
GET /api/v1/api-keys
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "key-uuid-1",
    "name": "My Development Key",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "last_used_at": null
  },
  {
    "id": "key-uuid-2",
    "name": "Production Key",
    "is_active": true,
    "created_at": "2024-01-02T00:00:00Z",
    "last_used_at": "2024-01-02T12:00:00Z"
  }
]
```

## 🔧 Error Handling Examples

### 1. Authentication Errors

**Frontend Error Handling**
```typescript
// From: frontend/src/lib/api.ts
const apiRequest = async (endpoint: string, options: RequestInit = {}, useJwtAuth: boolean = false) => {
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      if (response.status === 401) {
        // Token expired or invalid
        logout();
        throw new Error("Session expired. Please login again.");
      }
      
      const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;
      throw new Error(errorMessage);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API request failed for ${endpoint}:`, error);
    throw error;
  }
};
```

**Backend Error Response**
```python
# From: app/api/v1/endpoints/analyze.py
@router.post("/quick", response_model=AnalysisResult)
async def quick_analyze(analysis_data: AnalysisRequestCreate, request: Request):
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid JWT token."
        )
    
    try:
        result = await analyze_code(db, analysis_data, user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Analysis failed: {str(e)}"
        )
```

**HTTP Error Flow**
```http
POST /api/v1/analyze/quick
Content-Type: application/json

{
  "code": "print('hello')",
  "language": "python"
}

HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Authentication required. Please provide a valid JWT token."
}
```

### 2. Validation Errors

**Frontend Validation**
```typescript
// From: frontend/src/pages/Playground.tsx
const handleAnalyze = async () => {
  if (!codeInput.trim()) {
    toast.error("Please provide code to analyze");
    return;
  }
  
  if (!selectedLanguage) {
    toast.error("Please select a programming language");
    return;
  }
  
  // Proceed with API call...
};
```

**Backend Validation**
```python
# From: app/models/schemas/analysis.py
class AnalysisRequestCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    language: str = Field(..., regex="^(python|javascript|typescript|java|go|rust)$")
    traceback: Optional[str] = Field(None, max_length=10000)
    
    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('Code cannot be empty')
        return v
```

## 🚀 Real-World Usage Patterns

### 1. Frontend Component with API Integration

```typescript
// Complete example from Playground component
const Playground = () => {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  
  const handleAnalyze = async () => {
    setIsLoading(true);
    try {
      const analysisResult = await quickAnalyzeCode({
        code,
        language,
        traceback: undefined
      });
      setResult(analysisResult);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div>
      <textarea value={code} onChange={(e) => setCode(e.target.value)} />
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
      </select>
      <button onClick={handleAnalyze} disabled={isLoading}>
        {isLoading ? "Analyzing..." : "Analyze Code"}
      </button>
      {result && <AnalysisResults result={result} />}
    </div>
  );
};
```

### 2. Backend Service with Database Integration

```python
# Complete example from analysis service
async def analyze_code(db: Session, request: AnalysisRequestCreate, user_id: str, agent_system: AgentSystem):
    # Create analysis request in database
    db_analysis = AnalysisRequest(
        id=str(uuid4()),
        user_id=user_id,
        code=request.code,
        language=request.language,
        traceback=request.traceback,
        status=AnalysisStatus.PENDING,
        created_at=datetime.utcnow()
    )
    
    db.add(db_analysis)
    db.commit()
    
    try:
        # Process with agent system
        if agent_system and agent_system.running:
            issues = await process_with_agents(agent_system, request.code, request.language)
        else:
            issues = await process_direct_analysis(request.code, request.language)
        
        # Update database with results
        db_analysis.status = AnalysisStatus.COMPLETED
        db_analysis.result = {"issues": [issue.dict() for issue in issues]}
        db_analysis.completed_at = datetime.utcnow()
        
        db.commit()
        
        return AnalysisResult(
            request_id=db_analysis.id,
            status="completed",
            issues=issues
        )
        
    except Exception as e:
        db_analysis.status = AnalysisStatus.FAILED
        db_analysis.error = str(e)
        db.commit()
        raise
```

This comprehensive guide shows the exact flow of data between your frontend and backend, making it clear how the server-side and client-side components work together in AgentLogger. 