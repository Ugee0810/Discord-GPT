# Discord-GPT (LM Studio)

Discord 슬래시 명령(`/chat`)을 통해 로컬에서 실행 중인 LM Studio(OpenAI Compatible API) 모델과 대화하는 봇입니다.

## 프로젝트 구조

주요 코드는 `discord_gpt/` 패키지 아래에 있습니다.

```
discord_gpt/
  bot.py
  lmstudio_client.py
  memory_store.py
  utils.py
bot.py  # 실행 엔트리(래퍼)
```

## 준비물

- Python 3.10+
- LM Studio (Local Server 기능)
- Discord Bot Token

## 설치 (가상환경)

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 환경 변수 설정 (.env)

프로젝트 루트에 `.env` 파일을 만들고 아래 값을 설정합니다. (`.env.example` 참고, `.env`는 `.gitignore`로 커밋되지 않습니다.)

```ini
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN

# 선택: 커맨드를 특정 서버(길드)에 즉시 반영하려면 서버 ID를 입력
BOT_GUILD_ID=123456789012345678

# 선택: LM Studio OpenAI Compatible Server 주소 (기본값: http://127.0.0.1:1234/v1)
LM_BASE_URL=http://127.0.0.1:1234/v1

# 선택: 사용할 모델 이름 (기본값: llama-3.1-8b-instruct)
LM_MODEL=llama-3.1-8b-instruct
```

## LM Studio 설정

1. LM Studio에서 모델을 로드합니다.
2. LM Studio의 **Local Server**를 실행합니다.
3. 서버 주소가 `LM_BASE_URL`과 일치하는지 확인합니다. (기본값: `http://127.0.0.1:1234/v1`)
4. 서버가 `POST /v1/chat/completions` 요청을 받을 수 있어야 합니다.

## Discord Bot 생성/초대

1. Discord Developer Portal에서 Application을 생성합니다.
2. Bot을 추가하고 Token을 발급받아 `.env`의 `DISCORD_TOKEN`에 넣습니다.
3. OAuth2 URL Generator에서 아래를 체크해 서버로 초대합니다.
   - **Scopes**: `bot`, `applications.commands`
   - **Bot Permissions**: 필요한 권한만 선택 (기본적으로 메시지 전송 정도)

## 실행

가상환경을 활성화한 뒤 아래를 실행합니다.

```bash
python -m discord_gpt

# 또는 (동일 동작)
python bot.py
```

## 사용법

- `/chat message:<텍스트>`: LLM과 대화합니다.
- `/reset`: 현재 유저의 대화 메모리를 초기화합니다.
- `/ping`: 봇 상태를 확인합니다.

## 문제 해결

- 슬래시 명령이 바로 안 보이는 경우
  - `BOT_GUILD_ID`를 설정하면 해당 서버(길드)에 즉시 동기화됩니다.
  - 글로벌 동기화(`BOT_GUILD_ID=0`)는 반영까지 시간이 걸릴 수 있습니다.
- LM Studio 호출이 실패하는 경우
  - LM Studio 서버가 실행 중인지, `LM_BASE_URL`이 올바른지 확인하세요.
  - 모델이 로드되어 있고 요청한 `LM_MODEL` 값이 유효한지 확인하세요.
