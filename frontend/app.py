"""영화 리뷰 & 감성 분석 - Streamlit 프론트엔드.

모든 데이터는 FastAPI 백엔드에서 관리하며, 이 앱은 화면 표시와 API 호출만 담당한다.
"""
import os
from datetime import date, datetime

import pandas as pd
import requests
import streamlit as st


def _backend_url() -> str:
    try:
        return st.secrets["BACKEND_URL"].rstrip("/")
    except Exception:
        return os.getenv("BACKEND_URL", "http://localhost:8001").rstrip("/")


API = _backend_url()
PAGES = {
    "movies": "🎬 영화 목록",
    "add_movie": "➕ 영화 추가",
    "add_review": "✍️ 리뷰 등록",
    "recent": "📝 최근 리뷰",
}
SENTIMENT_KO = {"positive": "😊 긍정", "negative": "😞 부정"}

st.set_page_config(page_title="무비 리뷰 & 감성 분석", page_icon="🎬", layout="wide")


# ---------------- API helpers ----------------
def api(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{API}{path}", timeout=60, **kwargs)
    except requests.RequestException as e:
        st.error(f"백엔드 서버에 연결할 수 없습니다: {API}\n\n{e}")
        st.stop()
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail")
        except ValueError:
            detail = r.text
        st.error(f"요청 실패 ({r.status_code}): {detail}")
        return None
    return r.json() if r.content else {}


def fetch_movies() -> list[dict]:
    return api("GET", "/movies") or []


def stars(rating: float | None) -> str:
    if rating is None:
        return "평점 없음"
    full = int(round(rating))
    return "★" * full + "☆" * (5 - full) + f"  {rating:.2f} / 5"


def fmt_dt(s: str) -> str:
    return datetime.fromisoformat(s).strftime("%Y-%m-%d %H:%M")


def poster(url: str, height: int = 360):
    # 나무위키 이미지는 referrer 정책 때문에 no-referrer로 직접 렌더링
    st.markdown(
        f'<img src="{url}" referrerpolicy="no-referrer" '
        f'style="width:100%;height:{height}px;object-fit:cover;border-radius:10px;">',
        unsafe_allow_html=True,
    )


# ---------------- Pages ----------------
def page_movies():
    st.header("🎬 영화 목록")
    movies = fetch_movies()
    if not movies:
        st.info("등록된 영화가 없습니다. '영화 추가' 메뉴에서 영화를 등록해 주세요.")
        return
    cols = st.columns(3)
    for i, m in enumerate(movies):
        with cols[i % 3]:
            with st.container(border=True):
                poster(m["poster_url"])
                st.subheader(m["title"])
                st.markdown(f"**평균 평점** &nbsp; :orange[{stars(m['average_rating'])}]")
                st.caption(
                    f"🆔 {m['id']} · 📅 {m['release_date']} · 🎥 {m['director']}  \n"
                    f"🏷️ {m['genre']} · 💬 리뷰 {m['review_count']}개"
                )
                with st.expander("리뷰 보기"):
                    reviews = api("GET", f"/movies/{m['id']}/reviews") or []
                    if not reviews:
                        st.write("아직 리뷰가 없습니다.")
                    for r in reviews:
                        st.markdown(
                            f"{SENTIMENT_KO[r['sentiment_label']]} **{r['sentiment_score']:.2f}** · "
                            f"{r['author']}  \n{r['content']}"
                        )
                if st.button("🗑️ 영화 삭제", key=f"del_{m['id']}", use_container_width=True):
                    if api("DELETE", f"/movies/{m['id']}") is not None:
                        st.toast(f"'{m['title']}' 삭제 완료")
                        st.rerun()


def page_add_movie():
    st.header("➕ 영화 추가")
    with st.form("movie_form", clear_on_submit=True):
        title = st.text_input("제목 *")
        release_date = st.date_input("개봉일 *", value=date.today(), min_value=date(1900, 1, 1))
        director = st.text_input("감독 *")
        genre = st.text_input("장르 *", placeholder="예: 액션, 드라마")
        poster_url = st.text_input("포스터 URL *", placeholder="https://i.namu.wiki/...")
        submitted = st.form_submit_button("영화 등록", type="primary")
    if submitted:
        if not all([title.strip(), director.strip(), genre.strip(), poster_url.strip()]):
            st.warning("모든 항목을 입력해 주세요.")
            return
        movie = api(
            "POST",
            "/movies",
            json={
                "title": title.strip(),
                "release_date": release_date.isoformat(),
                "director": director.strip(),
                "genre": genre.strip(),
                "poster_url": poster_url.strip(),
            },
        )
        if movie:
            st.success(f"'{movie['title']}' 영화가 등록되었습니다. (ID: {movie['id']})")
            c1, c2 = st.columns([1, 3])
            with c1:
                poster(movie["poster_url"], height=280)


def page_add_review():
    st.header("✍️ 리뷰 등록")
    movies = fetch_movies()
    if not movies:
        st.info("먼저 영화를 등록해 주세요.")
        return
    options = {m["id"]: f"[{m['id']}] {m['title']}" for m in movies}
    with st.form("review_form", clear_on_submit=True):
        movie_id = st.selectbox("영화 선택 *", options, format_func=options.get)
        author = st.text_input("작성자 이름 *")
        content = st.text_area("리뷰 내용 *", height=120)
        submitted = st.form_submit_button("리뷰 등록 및 감성 분석", type="primary")
    if submitted:
        if not author.strip() or not content.strip():
            st.warning("작성자 이름과 리뷰 내용을 입력해 주세요.")
            return
        with st.spinner("감성 분석 중..."):
            review = api(
                "POST", "/reviews",
                json={"movie_id": movie_id, "author": author.strip(), "content": content.strip()},
            )
        if review:
            st.session_state["last_review"] = review
    review = st.session_state.get("last_review")
    if review:
        st.success("리뷰가 등록되었습니다. 감성 분석 결과는 다음과 같습니다.")
        with st.container(border=True):
            st.markdown(f"**{options.get(review['movie_id'], review['movie_id'])}** · {review['author']}")
            st.write(f"“{review['content']}”")
            c1, c2, c3 = st.columns(3)
            c1.metric("감성 분석 결과", SENTIMENT_KO[review["sentiment_label"]])
            c2.metric("긍정 확률", f"{review['positive_prob'] * 100:.1f}%")
            c3.metric("감성 점수 (0~5)", f"{review['sentiment_score']:.2f}")
            st.progress(review["positive_prob"])


def page_recent():
    st.header("📝 최근 리뷰 (10개)")
    reviews = api("GET", "/reviews", params={"limit": 10}) or []
    if not reviews:
        st.info("등록된 리뷰가 없습니다.")
        return
    titles = {m["id"]: m["title"] for m in fetch_movies()}
    df = pd.DataFrame(
        {
            "영화 ID": [r["movie_id"] for r in reviews],
            "영화": [titles.get(r["movie_id"], "-") for r in reviews],
            "등록일": [fmt_dt(r["created_at"]) for r in reviews],
            "작성자": [r["author"] for r in reviews],
            "리뷰 내용": [r["content"] for r in reviews],
            "감성 분석 결과": [SENTIMENT_KO[r["sentiment_label"]] for r in reviews],
            "감성 점수": [r["sentiment_score"] for r in reviews],
        }
    )
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "리뷰 내용": st.column_config.TextColumn(width="large"),
            "감성 점수": st.column_config.ProgressColumn(min_value=0, max_value=5, format="%.2f"),
        },
    )
    with st.expander("🗑️ 리뷰 삭제"):
        labels = {r["id"]: f"[{r['id']}] {r['author']} - {r['content'][:30]}" for r in reviews}
        rid = st.selectbox("삭제할 리뷰", labels, format_func=labels.get)
        if st.button("삭제"):
            if api("DELETE", f"/reviews/{rid}") is not None:
                st.toast("리뷰 삭제 완료")
                st.rerun()


# ---------------- Layout ----------------
qp_page = st.query_params.get("page", "movies")
keys = list(PAGES)
with st.sidebar:
    st.title("🎬 무비 리뷰")
    st.caption("영화 정보 · 리뷰 · 감성 분석")
    page = st.radio("메뉴", keys, index=keys.index(qp_page) if qp_page in keys else 0, format_func=PAGES.get)
    st.query_params["page"] = page
    st.divider()
    st.caption(f"Backend: `{API}`")

{"movies": page_movies, "add_movie": page_add_movie, "add_review": page_add_review, "recent": page_recent}[page]()
