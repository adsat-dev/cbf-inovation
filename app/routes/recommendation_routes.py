
from fastapi import APIRouter, HTTPException
from ..models.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from ..services.recommendation_service import recommendation_engine

router = APIRouter()


@router.post("/recommendations", response_model=list[RecommendationResponse])
async def get_recommendations(request: RecommendationRequest):
    recommendations = recommendation_engine.get_recommendations(
        title=request.title,
        top_n=request.top_n
    )

    if not recommendations:
        raise HTTPException(status_code=404, detail="Inovasi tidak ditemukan")

    return recommendations
