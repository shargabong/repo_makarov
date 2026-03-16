from typing import Generator

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from .model import ProductCreate, ProductOut, ProductUpdate
from .repository import ProductRepository, get_session
from .service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

def get_db_session() -> Generator[Session, None, None]:
    yield from get_session()

def get_service(session: Session = Depends(get_db_session)) -> ProductService:
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

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_service),
):
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_service),
):
    try:
        return service.update_product(product_id, product_data)
    except ValueError as error:
        if str(error) == "product_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            ) from error
        raise

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_service),
):
    try:
        service.delete_product(product_id)
    except ValueError as error:
        if str(error) == "product_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            ) from error
        raise

    return Response(status_code=status.HTTP_204_NO_CONTENT)


