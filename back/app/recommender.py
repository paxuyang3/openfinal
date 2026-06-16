from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    flavor: str = Field(..., description="sweet, refreshing, bitter, nutty, or creamy")
    caffeine: str = Field(..., description="yes, no, or any")
    temperature: str = Field(..., description="ice, hot, or any")
    milk: str = Field(..., description="ok, avoid, or any")


class DrinkRecommendation(BaseModel):
    name: str
    description: str
    has_caffeine: bool
    tags: list[str]
    score: int


class RecommendationResponse(BaseModel):
    reason: str
    recommendations: list[DrinkRecommendation]


DRINKS = [
    {
        "name": "바닐라 라떼",
        "description": "달콤한 바닐라 향과 우유의 부드러움이 잘 맞는 커피 음료입니다.",
        "has_caffeine": True,
        "tags": ["sweet", "creamy", "coffee", "milk", "hot", "ice"],
    },
    {
        "name": "초코 라떼",
        "description": "카페인 없이 달콤하고 진한 맛을 즐기기 좋은 음료입니다.",
        "has_caffeine": False,
        "tags": ["sweet", "creamy", "milk", "hot", "ice"],
    },
    {
        "name": "딸기 라떼",
        "description": "상큼한 과일 향과 우유의 부드러움이 함께 느껴지는 음료입니다.",
        "has_caffeine": False,
        "tags": ["sweet", "refreshing", "creamy", "milk", "ice"],
    },
    {
        "name": "레몬 에이드",
        "description": "탄산감과 레몬 향이 있는 시원하고 상큼한 음료입니다.",
        "has_caffeine": False,
        "tags": ["refreshing", "fruit", "ade", "ice"],
    },
    {
        "name": "자몽 에이드",
        "description": "달콤쌉싸름한 과일 맛을 시원하게 마시기 좋은 음료입니다.",
        "has_caffeine": False,
        "tags": ["refreshing", "fruit", "ade", "ice", "bitter"],
    },
    {
        "name": "아메리카노",
        "description": "우유 없이 깔끔하고 쌉싸름한 커피 맛을 느낄 수 있습니다.",
        "has_caffeine": True,
        "tags": ["bitter", "coffee", "hot", "ice"],
    },
    {
        "name": "콜드브루",
        "description": "산미가 적고 진한 커피 향을 차갑게 즐기기 좋은 음료입니다.",
        "has_caffeine": True,
        "tags": ["bitter", "coffee", "ice"],
    },
    {
        "name": "말차 라떼",
        "description": "쌉싸름한 말차와 우유의 고소함이 섞인 부드러운 음료입니다.",
        "has_caffeine": True,
        "tags": ["bitter", "nutty", "creamy", "milk", "hot", "ice"],
    },
    {
        "name": "고구마 라떼",
        "description": "카페인 없이 고소하고 포근한 단맛을 즐기기 좋은 음료입니다.",
        "has_caffeine": False,
        "tags": ["sweet", "nutty", "creamy", "milk", "hot"],
    },
    {
        "name": "캐모마일 티",
        "description": "카페인 부담 없이 따뜻하고 은은하게 마시기 좋은 차입니다.",
        "has_caffeine": False,
        "tags": ["light", "tea", "hot"],
    },
]


FLAVOR_LABELS = {
    "sweet": "달콤한 맛",
    "refreshing": "상큼한 맛",
    "bitter": "쌉싸름한 맛",
    "nutty": "고소한 맛",
    "creamy": "부드러운 맛",
}


def _score_drink(drink: dict, request: RecommendationRequest) -> int:
    tags = set(drink["tags"])
    score = 0

    if request.flavor in tags:
        score += 5
    if request.temperature != "any" and request.temperature in tags:
        score += 2
    if request.milk == "ok" and "milk" in tags:
        score += 2
    if request.milk == "avoid" and "milk" not in tags:
        score += 2
    if request.caffeine == "yes" and drink["has_caffeine"]:
        score += 3
    if request.caffeine == "no" and not drink["has_caffeine"]:
        score += 3

    return score


def recommend_drinks(request: RecommendationRequest) -> RecommendationResponse:
    candidates = DRINKS

    if request.caffeine == "no":
        candidates = [drink for drink in candidates if not drink["has_caffeine"]]
    elif request.caffeine == "yes":
        candidates = [drink for drink in candidates if drink["has_caffeine"]]

    scored = [
        DrinkRecommendation(
            name=drink["name"],
            description=drink["description"],
            has_caffeine=drink["has_caffeine"],
            tags=drink["tags"],
            score=_score_drink(drink, request),
        )
        for drink in candidates
    ]
    scored.sort(key=lambda item: item.score, reverse=True)

    label = FLAVOR_LABELS.get(request.flavor, "입력한 취향")
    caffeine_text = {
        "yes": "카페인이 있는 음료 중에서",
        "no": "카페인이 없는 음료 중에서",
        "any": "카페인 여부와 관계없이",
    }.get(request.caffeine, "카페인 조건에 맞춰")
    reason = f"{label}을 기준으로 {caffeine_text} 가장 잘 맞는 메뉴를 골랐습니다."

    return RecommendationResponse(reason=reason, recommendations=scored[:3])
