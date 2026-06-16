import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://backend:8000/recommend")

FLAVOR_OPTIONS = {
    "달콤한 맛": "sweet",
    "상큼한 맛": "refreshing",
    "쌉싸름한 커피 맛": "bitter",
    "고소한 맛": "nutty",
    "부드러운 맛": "creamy",
}

CAFFEINE_OPTIONS = {
    "상관없음": "any",
    "카페인 있는 음료": "yes",
    "카페인 없는 음료": "no",
}

TEMPERATURE_OPTIONS = {
    "상관없음": "any",
    "아이스": "ice",
    "따뜻한 음료": "hot",
}

MILK_OPTIONS = {
    "상관없음": "any",
    "우유 들어간 음료 괜찮음": "ok",
    "우유 없는 음료": "avoid",
}


def request_recommendation(payload: dict) -> dict:
    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="카페 음료 추천", page_icon="☕", layout="centered")

st.title("카페 음료 추천")
st.caption("취향을 선택하면 어울리는 음료를 추천합니다.")

with st.form("recommendation_form"):
    flavor_label = st.selectbox("오늘 원하는 맛", list(FLAVOR_OPTIONS.keys()))
    caffeine_label = st.radio("카페인 선호", list(CAFFEINE_OPTIONS.keys()), horizontal=True)
    temperature_label = st.radio("온도", list(TEMPERATURE_OPTIONS.keys()), horizontal=True)
    milk_label = st.radio("우유 포함 여부", list(MILK_OPTIONS.keys()), horizontal=True)

    submitted = st.form_submit_button("추천 받기", use_container_width=True)

if submitted:
    payload = {
        "flavor": FLAVOR_OPTIONS[flavor_label],
        "caffeine": CAFFEINE_OPTIONS[caffeine_label],
        "temperature": TEMPERATURE_OPTIONS[temperature_label],
        "milk": MILK_OPTIONS[milk_label],
    }

    try:
        result = request_recommendation(payload)
    except requests.exceptions.RequestException as exc:
        st.error(f"추천 서버에 연결할 수 없습니다: {exc}")
    else:
        st.subheader("추천 결과")
        st.info(result["reason"])

        for index, item in enumerate(result["recommendations"], start=1):
            with st.container(border=True):
                caffeine_text = "카페인 있음" if item["has_caffeine"] else "카페인 없음"
                st.markdown(f"### {index}. {item['name']}")
                st.write(item["description"])
                st.write(f"조건 점수: {item['score']}점 · {caffeine_text}")
