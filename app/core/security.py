"""
Authentication, Password Hashing, JWT Tokens & Role-Based Access Control (RBAC).
"""

import base64
import hashlib
import hmac
import json
import time
from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login", auto_error=False)

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Generate secure salted PBKDF2-HMAC-SHA256 hash."""
    if not salt:
        salt = base64.b64encode(hashlib.sha256(str(time.time()).encode()).digest()[:16]).decode()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    hash_b64 = base64.b64encode(dk).decode()
    return f"{salt}${hash_b64}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against salted PBKDF2 hash."""
    try:
        salt, expected_hash = hashed_password.split("$")
        calculated = hash_password(plain_password, salt)
        return hmac.compare_digest(calculated, hashed_password)
    except Exception:
        return False

def create_jwt_token(payload: Dict[str, Any], expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Create signed HS256 JWT token using standard cryptographic libraries."""
    header = {"alg": settings.JWT_ALGORITHM, "typ": "JWT"}
    exp = int(time.time()) + (expires_minutes * 60)
    claims = {**payload, "exp": exp, "iat": int(time.time())}
    
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    claims_b64 = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    signing_input = f"{header_b64}.{claims_b64}".encode()
    
    signature = hmac.new(settings.JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{header_b64}.{claims_b64}.{sig_b64}"

def decode_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode signed JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, claims_b64, sig_b64 = parts
        
        # Verify signature
        signing_input = f"{header_b64}.{claims_b64}".encode()
        expected_sig = hmac.new(settings.JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
        
        # Pad base64
        padded_sig = sig_b64 + "=" * (-len(sig_b64) % 4)
        actual_sig = base64.urlsafe_b64decode(padded_sig.encode())
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
            
        padded_claims = claims_b64 + "=" * (-len(claims_b64) % 4)
        claims = json.loads(base64.urlsafe_b64decode(padded_claims.encode()).decode())
        
        # Verify expiration
        if claims.get("exp", 0) < time.time():
            return None
        return claims
    except Exception:
        return None

def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Returns decoded claims or None if unauthenticated."""
    if not token:
        return None
    claims = decode_jwt_token(token)
    return claims

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Enforces valid JWT authentication."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    claims = decode_jwt_token(token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return claims

def require_role(allowed_roles: List[str]):
    """FastAPI dependency for Role-Based Access Control (RBAC)."""
    def role_checker(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = user.get("role")
        if user_role not in allowed_roles and user_role != "Administrator":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role in {allowed_roles}, your role: '{user_role}'."
            )
        return user
    return role_checker
