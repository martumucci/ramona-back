"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import orders as admin_orders
from app.api.admin import products as admin_products
from app.api.public import auth, cart, products
from app.config import settings
from app.shared.exceptions import register_exception_handlers

app = FastAPI(title="Ramona Shop API", version="1.0.0")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Public routes
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")

# Admin routes
app.include_router(admin_products.router, prefix="/api/admin")
app.include_router(admin_orders.router, prefix="/api/admin")


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
