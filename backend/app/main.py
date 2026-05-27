from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import transactions, assets, liabilities, balance_sheet, cashflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - creates tables on startup."""
    # Create database and tables on startup
    create_db_and_tables()
    yield
    # Cleanup (if needed) on shutdown


app = FastAPI(
    title="Cashflow MVP",
    description="A minimal personal cashflow bookkeeping app",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router)
app.include_router(assets.router)
app.include_router(liabilities.router)
app.include_router(balance_sheet.router)
app.include_router(cashflow.router)


@app.get("/")
async def root():
    return {"message": "Cashflow MVP API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}
