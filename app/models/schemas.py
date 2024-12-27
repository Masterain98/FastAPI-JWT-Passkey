from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    public_key: str
    device_id: str


class LoginRequest(BaseModel):
    username: str
    signed_challenge: str


class ChallengeResponse(BaseModel):
    username: str
    challenge: str


class ChallengeRequest(BaseModel):
    username: str
