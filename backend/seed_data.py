"""초기 데이터 등록 스크립트: 영화 3편(오디세이, 타짜: 벨제붑의 노래, 부활남: 더 레드) + 영화당 리뷰 10개.

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
        ],
    },
    {
        "title": "타짜: 벨제붑의 노래",
        "release_date": "2026-09-23",
        "director": "최국희",
        "genre": "범죄, 드라마, 느와르",
        "poster_url": "https://i.namu.wiki/i/XPk1uiPpt92LHDQaK6cSM48jjLkb5AwU9cHLX81TWoJ-XVrVDXq88sbQYNxahp9UF5f8cjbYcH0bwmhh8twjpA8_U69sGAiVzsH8I7l5M40BbhT4LMx6C8JkLDrwMAWSJs9cXeGaMTD-k5o7pYNtZg.webp",
        "reviews": [
            ("김태호", "추석엔 역시 타짜죠. 시리즈 마지막 편답게 판이 크고 긴장감이 끝까지 이어집니다."),
            ("이지은", "변요한 배우 연기가 정말 좋았어요. 친구에게 배신당한 분노가 고스란히 느껴졌습니다."),
            ("박준영", "노재원 배우의 악역이 소름 끼치게 매력적이에요. 올해 최고의 빌런!"),
            ("최서윤", "글로벌 도박판이라는 설정 덕분에 스케일이 확 커져서 보는 맛이 있었어요."),
            ("정하늘", "전작들에 비해 대사의 맛이 떨어지고 캐릭터가 너무 평면적이라 실망했어요."),
            ("강민호", "마지막 승부 장면은 숨죽이고 봤습니다. 반전도 깔끔하고 재밌어요. 강추!"),
            ("조예린", "온라인 카지노 설명이 너무 길어서 중반부가 지루했어요. 러닝타임 줄였으면."),
            ("윤성민", "조우진 배우가 나올 때마다 웃음이 터졌어요. 완급 조절이 훌륭합니다."),
            ("임채원", "1편의 아우라를 기대하면 실망합니다. 개연성도 부족하고 별로였어요."),
            ("한도윤", "화투 대신 포커로 바뀌었는데도 타짜 특유의 쫄깃함은 그대로네요. 재밌게 봤습니다."),
        ],
    },
    {
        "title": "부활남: 더 레드",
        "release_date": "2026-09-30",
        "director": "백종열",
        "genre": "판타지, 액션, 코미디",
        "poster_url": "https://i.namu.wiki/i/jx5j39WMJW0ToWvABanjMM2qJdYvpE6NzUZeCndIherm5c68BMRP34dVMG5sJh8QeAGALabvF82VgqA8QzG-Hrks5-lu-F8g1Fo5aFpVlOrYbjD9L1Jowfu_Mk9w3gBMv8V3dLQ2v5TquDpSeWezUg.webp",
        "reviews": [
            ("김나연", "구교환 배우의 능청스러운 연기가 정말 최고예요. 웃다가 울다가 했습니다."),
            ("이준서", "죽으면 72시간 뒤에 부활한다는 설정이 신선하고 재밌어요. 웹툰 팬으로서 만족합니다."),
            ("박소율", "액션 장면이 화끈하고 빨간 머리 비주얼이 강렬해요. 극장에서 보길 잘했어요."),
            ("최현우", "취준생의 현실을 유쾌하게 풀어내서 공감도 되고 위로도 받았어요. 추천합니다."),
            ("정다은", "개그 코드가 너무 유치하고 억지스러워서 보는 내내 민망했어요. 별로였습니다."),
            ("강시우", "신승호 배우의 악역 연기가 소름 돋을 정도로 좋았어요. 캐릭터 케미 최고!"),
            ("조하린", "후반부 전개가 너무 급하고 산만해서 지루했어요. 기대보다 실망스럽네요."),
            ("윤재희", "가볍게 즐기기 딱 좋은 오락 영화예요. 친구들이랑 보면 정말 재밌을 듯."),
            ("임건우", "원작 웹툰의 매력을 살리지 못했어요. 스토리가 엉성하고 시간이 아까웠습니다."),
            ("한소희", "음악과 편집이 감각적이고 템포가 빨라서 두 시간이 순식간이었어요. 강추!"),
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
