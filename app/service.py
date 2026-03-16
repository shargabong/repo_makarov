from model import Product, ProductCreate, ProductUpdate
from repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, product_data: ProductCreate) -> Product:
        return self.repo.create(product_data)

    def get_product(self, product_id: int) -> Product | None:
        return self.repo.get(product_id)