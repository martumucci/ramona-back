"""Product route handlers."""

from fastapi import APIRouter, Query

from app.api.dependencies import GetProductDep, ListProductsDep
from app.api.mappers import product_to_response
from app.api.schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
async def list_products(
    use_case: ListProductsDep,
    offset: int = Query(0, ge=0),
    limit: int | None = Query(None, ge=1),
) -> list[ProductResponse]:
    """List all products with optional pagination."""
    products = await use_case.execute(offset=offset, limit=limit)
    return [product_to_response(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, use_case: GetProductDep) -> ProductResponse:
    """Get a single product by ID."""
    product = await use_case.execute(product_id)
    return product_to_response(product)
