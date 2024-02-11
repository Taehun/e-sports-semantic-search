import os
import sys
from urllib.parse import quote

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 설정 및 모델 임포트를 위해 시스템 경로 수정
sys.path.append(os.getcwd())
from e_sports_semantic_search.config import settings  # noqa
from e_sports_semantic_search.models import Tournament

# PostgresQL 연결 정보
DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME

POSTGRES_URL = f"postgresql://{DB_USER}:{quote(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API 키 설정
X_API_KEY = settings.X_API_KEY

LEAGUE_ID = 98767991310872058  # "LCK" 리그의 ID


def fetch_tournament_data():
    """토너먼트 데이터를 외부 API로부터 가져옵니다."""
    url = "https://prod-relapi.ewp.gg/persisted/gw/getTournamentsForLeague"
    headers = {"x-api-key": X_API_KEY, "Content-Type": "application/json"}
    params = {"hl": "ko-KR", "leagueId": LEAGUE_ID}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=3)
        response.raise_for_status()  # 200 응답이 아닐 경우 에러를 발생시킵니다.
        return response.json().get("data", {}).get("leagues", [])
    except requests.RequestException as e:
        print(f"데이터 가져오기 실패: {e}")
        return []


def transfer_tournament_data(leagues_and_tournaments):
    """원본 데이터를 DB 스키마에 맞게 변환합니다."""
    tournament_data = []
    for league in leagues_and_tournaments:
        for tournament in league["tournaments"]:
            tournament_data.append(
                {
                    "id": int(tournament["id"]),
                    "leagueId": LEAGUE_ID,
                    "name": tournament["slug"],
                    "startDate": tournament["startDate"],
                    "endDate": tournament["endDate"],
                }
            )
    return tournament_data


def load_tournaments_to_db(tournaments):
    """토너먼트 데이터를 데이터베이스에 저장합니다."""
    if not tournaments:
        return
    session = SessionLocal()
    try:
        for tournament in tournaments:
            db_league = Tournament(**tournament)
            session.add(db_league)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"데이터베이스 저장 실패: {e}")
    finally:
        session.close()


def main():
    raw_league_tournament_data = fetch_tournament_data()
    tournament_data = transfer_tournament_data(raw_league_tournament_data)
    load_tournaments_to_db(tournament_data)


if __name__ == "__main__":
    main()
