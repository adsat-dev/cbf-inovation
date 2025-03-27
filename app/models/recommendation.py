from pydantic import BaseModel, Field

class RecommendationRequest(BaseModel):
    title: str 
    top_n: int = Field(default=5, ge=1, le=5)

class RecommendationResponse(BaseModel):
    inovasi: str
    jenis_inovasi: str
    deskripsi: str
    similarity_score: float