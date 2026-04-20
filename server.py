from fastapi import FastAPI, APIRouter, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
import routes

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db_client = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Unnati Investments API")

# Middleware to inject database into request state
@app.middleware("http")
async def add_db_to_request(request: Request, call_next):
    request.state.db = db_client
    response = await call_next(request)
    return response

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Basic health check route
@api_router.get("/")
async def root():
    return {"message": "Unnati Investments API", "status": "running"}

# Include content management routes
api_router.include_router(routes.router)

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
