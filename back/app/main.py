from fastapi import FastAPI

from app.recommender import RecommendationRequest, RecommendationResponse, recommend_drinks


app = FastAPI(title="Cafe Drink Recommendation API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest) -> RecommendationResponse:
    return recommend_drinks(request)
