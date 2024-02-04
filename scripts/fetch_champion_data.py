import os
import sys
from urllib.parse import quote

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.getcwd())
from e_sports_semantic_search.config import settings  # noqa
from e_sports_semantic_search.models import Champion

# PostgresQL 연결 정보
DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME

POSTGRES_URL = f"postgresql://{DB_USER}:{quote(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 데이터 가져오기 및 저장
def fetch_and_save_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/14.2.1/data/ko_KR/champion.json"
    response = requests.get(url, timeout=3)

    if response.status_code == 200:
        data = response.json()
        champions_data = data["data"]

        session = SessionLocal()
        for _, champion_info in champions_data.items():
            champion = Champion(
                key=int(champion_info["key"]),
                id=champion_info["id"],
                name=champion_info["name"],
                image=champion_info["image"]["full"],
            )
            session.add(champion)

        session.commit()
        session.close()
        print("데이터 저장 완료")
    else:
        print("데이터를 가져올 수 없습니다.")


if __name__ == "__main__":
    fetch_and_save_champion_data()
