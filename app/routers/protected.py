from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.auth import verify_jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    decoded = verify_jwt(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return {"message": f"Hello, {decoded['username']}! Welcome to the protected route."}
