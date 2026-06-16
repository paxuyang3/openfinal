from app.recommender import RecommendationRequest, recommend_drinks


def test_sweet_without_caffeine_recommends_non_coffee_option():
    request = RecommendationRequest(
        flavor="sweet",
        caffeine="no",
        temperature="ice",
        milk="ok",
    )

    result = recommend_drinks(request)

    names = [item.name for item in result.recommendations]
    assert "초코 라떼" in names
    assert all(not item.has_caffeine for item in result.recommendations)


def test_refreshing_flavor_prioritizes_ade():
    request = RecommendationRequest(
        flavor="refreshing",
        caffeine="any",
        temperature="ice",
        milk="avoid",
    )

    result = recommend_drinks(request)

    assert result.recommendations[0].name == "레몬 에이드"
    assert "상큼한 맛" in result.reason


def test_coffee_preference_can_return_caffeinated_drink():
    request = RecommendationRequest(
        flavor="bitter",
        caffeine="yes",
        temperature="hot",
        milk="avoid",
    )

    result = recommend_drinks(request)

    assert result.recommendations[0].name == "아메리카노"
    assert result.recommendations[0].has_caffeine is True
