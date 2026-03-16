from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from model import ProductCreate, ProductOut, ProductUpdate
from repository import ProductRepository, get_session
from service import ProductService


router = APIRouter(prefix="/products", tags=["products"])


def get_service():
    session = next(get_session())
    repo = ProductRepository(session)
    return ProductService(repo)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_service),
):
    return service.create_product(product_data)


@router.get("/", response_model=list[ProductOut])
def get_products(
    service: ProductService = Depends(get_service),
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    in_stock: bool | None = None,
):
    try:
        return service.get_products(
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
        )
    except ValueError as error:
        if str(error) == "invalid_price_range":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_price must be less than or equal to max_price",
            ) from error
        raise