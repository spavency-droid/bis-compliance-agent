from pydantic import BaseModel


class RetrievalResult(BaseModel):
    standard: dict
    keyword_score: float
    semantic_score: float
    combined_score: float

    @property
    def standard_id(self) -> str:
        return self.standard["standard_id"]