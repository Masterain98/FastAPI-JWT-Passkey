from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import RegisterRequest, LoginRequest, ChallengeRequest, ChallengeResponse
from app.db.database import users_db, challenges_db
from app.services.auth import create_jwt, verify_signature
from app.services.utils import generate_challenge

router = APIRouter()


@router.post("/register/")
async def register(request: RegisterRequest):
    if request.username in users_db:
        raise HTTPException(status_code=400, detail="User already registered.")
    print(f"Registering user: {request.username}; Device ID: {request.device_id}; Public Key: {request.public_key}")
    users_db[request.username] = {
        "public_key": request.public_key,
        "device_id": request.device_id,
    }
    return {"message": "User registered successfully."}


@router.post("/login/challenge/")
async def get_challenge(request: ChallengeRequest):
    username = request.username
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    challenge = generate_challenge()
    challenges_db[username] = challenge
    return ChallengeResponse(username=username, challenge=challenge)


@router.post("/login/verify/")
async def verify_login(request: LoginRequest):
    if request.username not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    if request.username not in challenges_db:
        raise HTTPException(status_code=400, detail="Challenge not found.")
    challenge = challenges_db.pop(request.username)
    public_key = users_db[request.username]["public_key"]
    if verify_signature(public_key, challenge, request.signed_challenge):
        token = create_jwt({"username": request.username})
        return {"message": "Login successful.", "token": token}
    else:
        raise HTTPException(status_code=400, detail="Invalid signature.")


@router.get("/db/user")
async def get_user():
    return users_db


@router.get("/db/challenge")
async def get_challenge():
    return challenges_db
