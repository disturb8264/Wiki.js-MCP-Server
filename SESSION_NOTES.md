# Session Notes

## 2026-04-10 Wiki.js MCP 서버 프로젝트 시작

이 폴더(`/home/disturb/wikijs-mcp`)는 기존 `/home/disturb/anilife`의 Wiki.js GraphQL API 테스트 성공 결과를 바탕으로, 범용 MCP 서버를 만들기 위한 새 프로젝트입니다.

### 현재 목표

- Python 기반 MCP 서버
- `fastmcp` 라이브러리 사용
- STDIO가 아니라 HTTP transport 사용
- Wiki.js GraphQL API를 MCP tools로 감싸서 재사용 가능하게 만들기

### 새 프로젝트 상태

- `.venv` 생성 완료
  - 시스템 `python3 -m venv`는 `ensurepip` 부재로 실패
  - 기존 `/home/disturb/anilife/.venv/bin/python`으로 새 `.venv` 생성
- `fastmcp==3.2.3` 설치 완료
- `pip install -e .` 완료
- 기존 `/home/disturb/anilife/.env`를 이 프로젝트 `.env`로 복사함
  - 토큰 내용은 출력하지 않았음
  - `.env`는 `.gitignore`에 포함

### 주요 파일

- `pyproject.toml`
  - 패키지 이름: `wikijs-mcp`
  - dependencies: `fastmcp`, `httpx`, `python-dotenv`
  - console script: `wikijs-mcp = wikijs_mcp.server:main`
- `src/wikijs_mcp/client.py`
  - Wiki.js GraphQL HTTP client
  - `.env`의 `WIKIJS_URL`, `WIKIJS_API_TOKEN` 사용
- `src/wikijs_mcp/server.py`
  - FastMCP HTTP 서버
  - `mcp.run(transport="http", host=..., port=..., path=...)`
  - 기본 endpoint: `http://127.0.0.1:8000/mcp`
  - health route: `GET /health`
- `.env.example`
  - Wiki.js 및 MCP 서버 환경변수 예시
- `README.md`
  - 실행 방법과 tool 목록

### 등록된 MCP tools

- `wikijs_health`
- `wikijs_graphql`
- `wikijs_list_pages`
- `wikijs_get_page_by_id`
- `wikijs_create_page`
- `wikijs_update_page`
- `wikijs_move_page`

### 검증 완료

```bash
.venv/bin/python -m compileall src
.venv/bin/python -m pip install -e .
```

Wiki.js GraphQL 연결 확인:

```text
pages 7
```

FastMCP HTTP 서버 health route 확인:

```text
{"status":"ok","service":"wikijs-mcp"}
```

FastMCP tool 호출 경로 확인:

```text
wikijs_list_pages -> 7 pages
```

### 실행 방법

```bash
cd /home/disturb/wikijs-mcp
source .venv/bin/activate
python -m wikijs_mcp.server
```

또는:

```bash
wikijs-mcp
```

환경변수로 바인딩 변경:

```bash
MCP_HOST=0.0.0.0 MCP_PORT=8787 MCP_PATH=/mcp python -m wikijs_mcp.server
```

### 다음 작업 후보

- MCP Inspector 또는 실제 MCP client에서 HTTP transport 연결 테스트
- Wiki.js 검색 tool 추가
- path 기반 page 조회 tool 추가
- create/update/move 같은 쓰기 tool에 확인 플래그 또는 dry-run 정책 추가
- GraphQL schema에 맞춰 page metadata, tree, tags 관련 tools 확장

---

이 폴더는 Synology NAS에서 Docker로 실행 중인 Wiki.js를 Python으로 제어해보기 위해 만든 테스트 프로젝트입니다.

## 환경

- 현재 프로젝트 경로: `/home/disturb/anilife`
- Python 가상환경: `.venv`
- 사용 Python: `Python 3.11.0rc1`
- Wiki.js GraphQL endpoint is configured through `.env` as `WIKIJS_URL`
- API 토큰은 `.env`의 `WIKIJS_API_TOKEN`에 있음
- `.env`는 민감정보가 있으므로 공유하거나 커밋하지 말 것

## 주요 파일

- `wikijs_api_test.py`
  - Wiki.js GraphQL API 테스트 CLI
  - 지원 명령:
    - 기본 실행: 페이지 목록 조회
    - `query`: raw GraphQL query 실행
    - `create-page`: 새 Wiki.js 문서 생성
    - `update-page`: 기존 문서 수정
    - `move-page`: 문서 경로 이동
- `wiki_tips_t1.md`
  - Wiki.js에 올린 프로젝트 설명 문서 원본
- `README.md`
  - 기본 실행 방법과 예시
- `.env.example`
  - 환경변수 예시

## 확인된 Wiki.js 문서 상태

현재 Wiki.js에는 다음 테스트 관련 문서가 있음.

- `id: 7`
  - `path: projects`
  - `title: PROJECTS`
  - 프로젝트 문서 모음용 상위 페이지
- `id: 4`
  - `path: projects/wikijs-api-test`
  - `title: Wiki.js API 연동 테스트`
  - 원래 `tips/t1`에 있던 문서를 PROJECTS 밑으로 이동한 것
- `id: 6`
  - `path: api-tests/codex-smoke-test`
  - `title: Codex API Smoke Test`
  - API 생성 테스트 문서

이전 경로 `tips/t1`은 더 이상 존재하지 않는 것을 확인함.

## 실행 예시

```bash
source .venv/bin/activate
python wikijs_api_test.py
```

페이지 목록 조회:

```bash
python wikijs_api_test.py query --query '{ pages { list { id path title } } }'
```

새 문서 생성:

```bash
python wikijs_api_test.py create-page \
  --path api-tests/hello \
  --title "Hello from API" \
  --content "# Hello"
```

문서 수정:

```bash
python wikijs_api_test.py update-page \
  --id 4 \
  --title "Wiki.js API 연동 테스트" \
  --content-file wiki_tips_t1.md \
  --tags api,wikijs,python
```

문서 이동:

```bash
python wikijs_api_test.py move-page \
  --id 4 \
  --path projects/wikijs-api-test
```

## 새 폴더로 옮길 때

추천 폴더명은 공백 없는 `wiki-my` 또는 `wikijs-api-test`.

```bash
cd /home/disturb
cp -a anilife wiki-my
code wiki-my
```

복사한 `.venv`가 경로 문제를 일으키면 새 폴더에서 재생성:

```bash
cd /home/disturb/wiki-my
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python wikijs_api_test.py
```

## 새 Codex 대화에서 이렇게 말하기

```text
이 폴더는 이전에 Wiki.js GraphQL API 테스트 프로젝트로 만들었어.
SESSION_NOTES.md를 먼저 읽고 맥락 이어서 작업해줘.
특히 wikijs_api_test.py, .env.example, README.md를 보고 현재 구조를 파악해줘.
.env에는 Wiki.js API 토큰이 있으니 내용은 출력하지 말고 사용만 해줘.
```

## 주의

- `.env`의 토큰은 절대 출력하지 말 것
- Wiki.js에 문서를 생성/수정/이동하는 명령은 실제 NAS Wiki.js 데이터를 바꿈
- Wiki.js `pages.update`로 path 변경 시 응답 path가 오래된 값처럼 보일 수 있었지만, 실제 목록에서는 이동이 반영됨
- 안정적인 이동은 `pages.move` mutation을 감싼 `move-page` 명령 사용 권장
