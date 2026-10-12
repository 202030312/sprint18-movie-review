"""초기 데이터 등록 스크립트: 영화 3편(오디세이, 타짜: 벨제붑의 노래, 암살자(들)) + 영화당 리뷰 11개.

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
            ("오지아", "음악과 미술이 세련돼서 영상만 봐도 즐거웠어요. 시리즈 피날레로 만족합니다."),
        ],
    },
    {
        "title": "암살자(들)",
        "release_date": "2026-09-23",
        "director": "허진호",
        "genre": "범죄, 드라마, 미스터리, 시대극",
        "poster_url": "https://i.namu.wiki/i/UrzyoJ_2gFubASz8U6LXq4ibgj0UtrydSpn93_iGAwvAAosaMeUXzZImVApXL0rTl9def5MpmGV6XcAEVAXxJ-8i1X2n-V9ZHKgdnbSY0842SVi67dDVo-KvfYZ53M0SKuafVaOAInT49Ts5oiDCTQ.webp",
        "reviews": [
            ("김나연", "실제 사건을 이렇게 긴장감 있게 풀어내다니 놀라웠어요. 몰입도 최고입니다."),
            ("이준서", "유해진 배우의 진지한 연기가 정말 압권이었어요. 다시 보고 싶은 영화."),
            ("박소율", "박해일, 이민호 배우의 연기 대결이 팽팽해서 두 시간이 금방 지나갔습니다."),
            ("최현우", "1974년의 분위기를 재현한 미술과 촬영이 훌륭해요. 시대극 좋아하면 강추."),
            ("정다은", "역사적 사실과 허구가 섞여 있어서 헷갈렸고 결말이 찝찝했어요. 아쉬웠습니다."),
            ("강시우", "마지막 30분은 정말 숨도 못 쉬고 봤어요. 허진호 감독의 연출이 빛납니다."),
            ("조하린", "전개가 너무 느리고 무거워서 보는 내내 답답했어요. 저랑은 안 맞네요."),
            ("윤재희", "추리 요소가 탄탄해서 끝까지 범인을 예측하기 어려웠어요. 정말 재밌습니다."),
            ("임건우", "소재는 흥미로운데 인물이 너무 많아 산만하고 지루했습니다. 별로예요."),
            ("한소희", "보고 나서 실제 사건을 찾아보게 만드는 힘이 있는 영화입니다. 추천해요."),
            ("오태윤", "배우들 연기, 음악, 미장센 모두 완성도가 높아요. 올가을 최고의 한국 영화!"),
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
