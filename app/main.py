from fastapi import FastAPI
from app.routers import auth, protected
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/resources", tags=["Protected Resources"])

# Mount static folder for serving static files
app.mount("/demo", StaticFiles(directory="demo"), name="demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/demo")
async def redirect_demo():
    return RedirectResponse(url="/demo/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)