import os
import sys
from urllib.parse import quote

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 설정 및 모델 임포트를 위해 시스템 경로 수정
sys.path.append(os.getcwd())
from e_sports_semantic_search.config import settings  # noqa
from e_sports_semantic_search.models import Match, Team

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
TOURNAMENT_ID = 110371551277508787  # lck_summer_2023


def fetch_match_data():
    """매치 데이터를 외부 API로부터 가져옵니다."""
    url = "https://prod-relapi.ewp.gg/persisted/gw/getCompletedEvents"
    headers = {"x-api-key": X_API_KEY, "Content-Type": "application/json"}
    params = {"hl": "ko-KR", "tournamentId": TOURNAMENT_ID}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=3)
        response.raise_for_status()
        return response.json().get("data", {}).get("schedule", {})["events"]
    except requests.RequestException as e:
        print(f"데이터 가져오기 실패: {e}")
        return []


def load_lck_teams() -> dict:
    """DB에서 LCK 팀 데이터를 가져옵니다."""
    session = SessionLocal()
    team_code_map = {}
    for team_obj in session.query(Team).order_by(Team.id):
        team_code_map[team_obj.code] = team_obj.id

    return team_code_map


def transfer_match_data(events, team_code):
    """원본 데이터를 DB 스키마에 맞게 변환합니다."""
    match_data = []
    for event in events:
        team1_id = int(team_code.get(event["match"]["teams"][0]["code"]))
        team2_id = int(team_code.get(event["match"]["teams"][1]["code"]))
        team1_score = event["match"]["teams"][0]["result"]["gameWins"]
        team2_score = event["match"]["teams"][1]["result"]["gameWins"]

        match_data.append(
            {
                "id": int(event["match"]["id"]),
                "tournamentId": TOURNAMENT_ID,
                "startTime": event["startTime"],
                "state": "finished",
                "team1Id": team1_id,
                "team2Id": team2_id,
                "team1Score": team1_score,
                "team2Score": team2_score,
                "winnerId": team1_id if team1_score > team2_score else team2_id,
            }
        )

    return match_data


def load_match_to_db(matches):
    """매치 데이터를 데이터베이스에 저장합니다."""
    if not matches:
        return
    session = SessionLocal()
    try:
        for match in matches:
            db_match = Match(**match)
            session.add(db_match)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"데이터베이스 저장 실패: {e}")
    finally:
        session.close()


def main():
    team_code = load_lck_teams()
    raw_events = fetch_match_data()
    match_data = transfer_match_data(raw_events, team_code)
    load_match_to_db(match_data)


if __name__ == "__main__":
    main()
