from model import Product, ProductCreate, ProductUpdate
from repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, product_data: ProductCreate) -> Product:
        return self.repo.create(product_data)

    def get_product(self, product_id: int) -> Product | None:
        return self.repo.get(product_id)
    
    def get_products(
        self,
        min_price: int | None = None,
        max_price: int | None = None,
        in_stock: bool | None = None,
    ) -> list[Product]:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("invalid_price_range")

        return self.repo.get_all(
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
        )

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("product_not_found")
        return self.repo.update(product, product_data)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("product_not_found")
        self.repo.delete(product)