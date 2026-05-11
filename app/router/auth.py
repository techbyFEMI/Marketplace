from fastapi import APIRouter, HTTPException,status
from core.db import get_supabase_async
from schemas.schema import(
    registerRequest,
    tokenResponse,
    loginrequest,
    userResponse
)
from core.auth import create_access_token
from core.auth import password_hash, verify_password







router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register", response_model=tokenResponse)
async def register_user(body: registerRequest)->tokenResponse:

    sb= await get_supabase_async()

    try:
        result = await (
            sb.table("users")
            .insert({
            "username":body.username,
            "hashed_password":password_hash(body.password),
            "role": body.role.value
        })
        .execute()
    )
    
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user registration failed"
            )
        user =result.data[0]
    except Exception as e:
        print(f"Error inserting user: {e}")

        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already taken"
        )
    token= create_access_token(
        User_id=user["id"],
        Username=user["username"],
        role=user["role"]
    )
    return tokenResponse(accessToken=token)

@router.post("/login", response_model=tokenResponse)
async def login_user(body: loginrequest)->tokenResponse:
        sb=await get_supabase_async()

        result=await(
            sb.table("users")
            .select("*")
            .eq("username", body.username)
            .maybe_single()
            .execute()
        )
        user=result.data
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details="user not found"
            )
        if not verify_password(body.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="invalid credentials"
            )
        
        token = create_access_token(
             User_id=user["id"],
             Username=user["username"],
             role=user["role"]
        )

        return tokenResponse(accessToken=token)