---
title: e-sports-semantic-search
app_file: ./e_sports_semantic_search/main.py
sdk: gradio
sdk_version: 4.10.0
---

[![Deploy on Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/deploy-on-spaces-md.svg)](https://huggingface.co/spaces/taehun-dev/e-sports-semantic-search)

## 시스템 아키텍처

![아미켁처](./architecture.png)

## 기술 스택

- UI: [Gradio](https://www.gradio.app)
- RAG: [LlamaIndex](https://www.llamaindex.ai)


## 시작하기

### 시스템 요구사항

- Python 3.11
- [Poetry](https://python-poetry.org/)
- [psycopg2](https://gist.github.com/prakashanantha/f957e6a9a193ac1bd8bf)

### 로컬 실행

OpenAI API 키가 필요합니다. [여기](https://platform.openai.com/api-keys)에서 API 키를 생성후 아래와 같이 환경 변수로 설정해주세요.

```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

`poetry run` 커맨드로 실행 합니다.

```shell
poetry run python e_sports_semantic_search/main.py
```

웹 브라우저에서 `http://127.0.0.1:7860` 주소에 접속합니다.

## 데이터 관리

### SQL DB

`alembic`을 사용하여 DB 스키마 버전 관리를 합니다:

#### SQL DB 스키마 업데이트

`./e_sports_semantic_search/models` 폴더의 데이터 모델 파일 변경시 아래 커맨드로 자동 생성 됩니다.

```shell
poetry run alembic revision --autogenerate -m "Update DB schema" --rev-id="0002"
```

- `-m`: 스키마 변경 내용
- `--rev-id`: 스키마 버전. `alembic/versions` 폴더 참고하여 최신 스키마 버전 +1로 설정

#### SQL DB 스키마 적용

현재 alembic 버전에서 `alembic/versions` 폴더의 스키마 파일의 `upgrade()` 함수 로직대로 다운그레이드 됩니다.

```shell
poetry run alembic upgrade head
```

#### SQL DB 스키마 롤백

현재 alembic 버전에서 `alembic/versions` 폴더의 스키마 파일의 `downgrade()` 함수 로직대로 다운그레이드 됩니다.

```shell
poetry run alembic upgrade head
```
