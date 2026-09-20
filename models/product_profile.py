from pydantic import BaseModel, Field


class ProductProfile(BaseModel):
    product_name: str = ""
    product_type: str = ""
    materials: list[str] = Field(default_factory=list)
    age_group: str = ""
    power_type: str = ""
    intended_use: str = ""
    features: list[str] = Field(default_factory=list)