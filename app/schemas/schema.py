from pydantic import BaseModel,field_validator
import re
from enum import Enum


class UserRole(str, Enum):
    Customer="customer"
    Vendor="vendor"

class registerRequest(BaseModel):
    username:str
    password:str
    role: UserRole
    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if not value:
            raise ValueError('Username is required')
        if len(value) < 3:
            raise ValueError('username must be at least 3 characters long')
        return value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, Value):
        if re.search(r'[A-Z]', Value) is None:
            raise ValueError('Password must contain at least one uppercase letter')
        if re.search(r'[a-z]', Value) is None:
            raise ValueError('Password must contain at least one lowercase letter')
        if re.search(r'[@$!%*?&]', Value) is None:
            raise ValueError('Password must contain at least one special character (@$!%*?&)')
        return Value



class tokenResponse(BaseModel):
    accessToken:str
    tokenType:str="bearer"

class loginrequest(BaseModel):
    username:str
    password:str


class userResponse(BaseModel):
    username:str
    password:str
    created_at:str

