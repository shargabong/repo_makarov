from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select

from model import Product, ProductCreate, ProductUpdate
from settings import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_all(
        self,
        min_price: int | None = None,
        max_price: int | None = None,
        in_stock: bool | None = None,
    ) -> list[Product]:
        statement = select(Product)

        if min_price is not None:
            statement = statement.where(Product.price >= min_price)
        if max_price is not None:
            statement = statement.where(Product.price <= max_price)
        if in_stock is not None:
            statement = statement.where(Product.in_stock == in_stock)

        return list(self.session.exec(statement).all())

    def update(self, product: Product, product_data: ProductUpdate) -> Product:
        product.name = product_data.name
        product.price = product_data.price
        product.in_stock = product_data.in_stock

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()