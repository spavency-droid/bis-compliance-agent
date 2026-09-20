from pydantic import BaseModel, Field


class BISStandard(BaseModel):
    standard_id: str
    title: str
    category: str
    product_types: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    power_types: list[str] = Field(default_factory=list)
    age_groups: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    scope: str = ""
    certification_scheme: str = ""
    mandatory_status: str = ""
    source_url: str = ""
    source_date: str = ""