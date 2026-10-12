"""초기 데이터 등록 스크립트: 영화 3편 + 영화당 리뷰 11개.

백엔드 API를 통해 등록하므로 리뷰마다 감성 분석이 실제로 실행됩니다.
(MOVIES 데이터는 AUTO_SEED=1일 때 app.main에서도 사용)
사용법: python seed_data.py [BACKEND_URL]   (기본값 http://localhost:8001)
"""
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"

MOVIES = [
    {
        "title": "오디세이",
        "release_date": "2026-08-05",
        "director": "크리스토퍼 놀란",
        "genre": "액션, 모험, 판타지, 서사시",
        "poster_url": "https://i.namu.wiki/i/JoNFFkOiiIGEqrV7cBwwdwwK8_o_GkBTY1oKSQniHjzLVnqlZKl7jOObK1gZUjy2kmoPs-8IKuuUvy-7q87WFPzZgcPkiBOii4ZkPZsEXfILz7xVMtQ9Z--p-qikNDRnK1dXPwBse50EJKO4Oo5DNA.webp",
        "reviews": [
            ("김민준", "아이맥스로 봤는데 바다 장면은 진짜 숨이 막힐 정도로 압도적이었어요. 올해 최고의 영화!"),
            ("이서연", "놀란 감독이 그리스 신화를 이렇게 풀어낼 줄 몰랐네요. 3시간이 순식간에 지나갔습니다."),
            ("박지호", "맷 데이먼의 오디세우스 연기가 정말 좋았어요. 귀향의 감정이 고스란히 전해졌습니다."),
            ("최유나", "음악이랑 사운드가 미쳤다. 극장에서 꼭 봐야 하는 영화입니다."),
            ("정우진", "러닝타임이 너무 길고 중반부가 지루했어요. 기대가 커서 그런지 실망했습니다."),
            ("강하은", "외눈박이 거인 장면은 실사 촬영이라 그런지 긴장감이 장난 아니었어요. 강력 추천합니다."),
            ("조민서", "스토리가 너무 산만하고 인물 감정선이 잘 안 느껴져서 별로였어요."),
            ("윤도현", "영상미 하나만으로도 티켓값이 아깝지 않아요. 두 번 봤습니다."),
            ("임수아", "원작을 모르면 이해하기 어려운 부분이 많아요. 대사가 잘 안 들려서 답답했습니다."),
            ("한지민", "놀란 영화 중 가장 감동적이었어요. 마지막 재회 장면에서 눈물이 났습니다."),
            ("오세훈", "배우들 연기, 미술, 촬영 모두 완벽합니다. 역시 놀란이네요."),
        ],
    },
    {
        "title": "타짜",
        "release_date": "2006-09-28",
        "director": "최동훈",
        "genre": "범죄, 드라마, 느와르",
        "poster_url": "https://i.namu.wiki/i/YvQ9Cs3gfknVqy5uyLlI80Rql5sOMAsRxcpQWYctCq5rxIuFYuzWw-j_FXtKeq35d3ZpmOqBJMzM6u0EhbldPDNmydTwofbNTmhhcLGpq8IZRe46Off8xAJ-NdBKcqO6sKWsDEp-5GtRenJON7B8Zg.webp",
        "reviews": [
            ("김태호", "몇 번을 봐도 질리지 않는 한국 범죄 영화의 명작입니다."),
            ("이지은", "김혜수 배우의 정마담 캐릭터는 정말 전설이에요. 대사 하나하나가 명대사."),
            ("박준영", "아귀 등장 장면은 지금 봐도 소름 돋습니다. 김윤석 연기 최고!"),
            ("최서윤", "조승우의 고니 연기가 너무 자연스러워서 몰입감이 대단했어요."),
            ("정하늘", "폭력적인 장면이 너무 많아서 보기 불편했어요. 저랑은 안 맞았습니다."),
            ("강민호", "최동훈 감독 특유의 빠른 전개와 맛깔나는 대사가 일품입니다."),
            ("조예린", "마지막 기차 화투 장면은 한국 영화 최고의 엔딩 중 하나라고 생각해요."),
            ("윤성민", "너무 과대평가된 영화 같아요. 생각보다 재미없고 지루했어요."),
            ("임채원", "유해진 배우의 고광렬 캐릭터 덕분에 웃다가 울다가 했네요. 강추!"),
            ("한도윤", "리마스터링 재개봉으로 극장에서 다시 봤는데 여전히 최고입니다."),
            ("오지아", "스토리가 너무 뻔하고 여성 캐릭터 묘사가 아쉬웠습니다. 별로예요."),
        ],
    },
    {
        "title": "인턴",
        "release_date": "2015-09-24",
        "director": "낸시 마이어스",
        "genre": "코미디, 드라마",
        "poster_url": "https://i.namu.wiki/i/lJYwmTe-AuwtTVjMHphUdBF305NDktOyXdRjFLr7cE09ZyAkr5MGNOwbVBtmJXnPapH7f7cX89qERep40Pmkdsl36iDO3ClisX6ZOQY350AfRGRNfxQqLz5me5j2xeT8SsK_DivKcRVV4s02e42O4w.webp",
        "reviews": [
            ("김나연", "보고 나면 마음이 따뜻해지는 힐링 영화예요. 로버트 드 니로 너무 멋져요."),
            ("이준서", "벤 같은 어른이 되고 싶다는 생각이 들었습니다. 인생 영화입니다."),
            ("박소율", "앤 해서웨이의 줄스 캐릭터에 많이 공감했어요. 일하는 여성들이 꼭 봤으면."),
            ("최현우", "잔잔하고 따뜻해서 좋아요. 주말에 혼자 보기 딱 좋은 영화."),
            ("정다은", "너무 뻔하고 갈등이 약해서 지루했어요. 기대 이하였습니다."),
            ("강시우", "손수건은 남을 위해 갖고 다니는 거라는 대사가 아직도 기억에 남아요. 최고!"),
            ("조하린", "경험이 결코 늙지 않는다는 메시지가 정말 감동적이었어요."),
            ("윤재희", "스토리가 너무 이상적이고 현실성이 없어서 별로였습니다."),
            ("임건우", "몇 번을 봐도 기분 좋아지는 영화입니다. 배우들 케미가 좋아요."),
            ("한소희", "중반 이후 전개가 늘어지고 결말이 허무했어요. 시간 아까웠습니다."),
            ("오태윤", "직장 생활에 지칠 때마다 꺼내 보는 영화예요. 강력 추천합니다."),
        ],
    },
]


def main():
    import requests

    for m in MOVIES:
        reviews = m.pop("reviews")
        r = requests.post(f"{BASE}/movies", json=m, timeout=30)
        r.raise_for_status()
        movie = r.json()
        print(f"[영화 등록] id={movie['id']} {movie['title']}")
        for author, content in reviews:
            rv = requests.post(
                f"{BASE}/reviews",
                json={"movie_id": movie["id"], "author": author, "content": content},
                timeout=60,
            )
            rv.raise_for_status()
            d = rv.json()
            print(f"   - {d['sentiment_label']:8s} {d['sentiment_score']:.2f}  {content[:30]}")
    print("완료")


if __name__ == "__main__":
    main()
