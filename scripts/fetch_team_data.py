import os
import sys
from urllib.parse import quote

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 설정 및 모델 임포트를 위해 시스템 경로 수정
sys.path.append(os.getcwd())
from e_sports_semantic_search.config import settings  # noqa
from e_sports_semantic_search.models import Team

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


def fetch_teams_data():
    """팀 데이터를 외부 API로부터 가져옵니다."""
    url = "https://prod-relapi.ewp.gg/persisted/gw/getTeams"
    headers = {"x-api-key": X_API_KEY, "Content-Type": "application/json"}
    params = {"hl": "ko-KR"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=3)
        response.raise_for_status()  # 200 응답이 아닐 경우 에러를 발생시킵니다.
        return response.json().get("data", {}).get("teams", [])
    except requests.RequestException as e:
        print(f"데이터 가져오기 실패: {e}")
        return []


def filter_lck_teams(teams):
    """LCK 리그에 속하는 팀만 필터링합니다."""
    filtered_teams = []
    for team in teams:
        # 팀 객체와 'homeLeague' 속성 값이 존재하며, 소속 리그가 'LCK'인 경우에만 필터링합니다.
        if team and team.get("homeLeague") and team.get("homeLeague").get("name") == "LCK":
            filtered_teams.append(
                {
                    "id": int(team["id"]),
                    "region": team["homeLeague"]["region"],
                    "code": team["code"],
                    "name": team["name"],
                    "image": team["image"],
                }
            )
    return filtered_teams


def load_teams_to_db(teams):
    """팀 데이터를 데이터베이스에 저장합니다."""
    if not teams:
        return
    session = SessionLocal()
    try:
        for team in teams:
            db_team = Team(**team)
            session.add(db_team)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"데이터베이스 저장 실패: {e}")
    finally:
        session.close()


def main():
    teams_data = fetch_teams_data()
    lck_teams = filter_lck_teams(teams_data)
    load_teams_to_db(lck_teams)


if __name__ == "__main__":
    main()
