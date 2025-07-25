from fastapi import FastAPI
from api.scan import router as scan_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Phishing Detector API")

# CORS configuration
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(scan_router, prefix="/api")

app.get("/")
async def root():
    return {"message": "Welcome to the Phishing Detector API. Use /api/scan-image to scan images."}