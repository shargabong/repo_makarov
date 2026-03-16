from pydantic import field_validator
from sqlmodel import Field, SQLModel


class ProductCreate(SQLModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(ge=0)
    in_stock: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 2:
            raise ValueError("Name must contain at least 2 characters.")
        return normalized

class ProductUpdate(SQLModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(ge=0)
    in_stock: bool = True

    @field_validator("имя")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 2:
            raise ValueError("Имя должно содержать не менее 2 символов.")
        return normalized

class Product(ProductCreate, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)

class ProductOut(ProductCreate):
    id: int