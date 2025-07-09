from pydantic import BaseModel, Field
from typing import List, Optional


class RecommendationRequest(BaseModel):
    innovation_id: str = Field(..., description="UUID dokumen inovasi")
    top_n: int = Field(default=5, ge=1, le=10)


class RecommendationResponse(BaseModel):
    id: str
    inovasi: str
    kategori: str
    deskripsi: str
    namaInnovator: str
    images: Optional[List[str]] = Field(default_factory=list)
    tahunDibuat: Optional[str] = Field(default=None)
    similarity_score: float


class RecommendationListResponse(BaseModel):
    message: str
    data: List[RecommendationResponse]
