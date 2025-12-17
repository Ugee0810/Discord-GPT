import os
import discord
from discord import app_commands
from dotenv import load_dotenv

from .lmstudio_client import LMStudioClient
from .memory_store import MemoryStore
from .utils import clamp_discord_message

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LM_BASE_URL = os.getenv("LM_BASE_URL", "http://127.0.0.1:1234/v1")
LM_MODEL = os.getenv("LM_MODEL", "llama-3.1-8b-instruct")
BOT_GUILD_ID = int(os.getenv("BOT_GUILD_ID", "0"))

# ====== 봇 기본 설정 ======
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

lm = LMStudioClient(base_url=LM_BASE_URL, model=LM_MODEL)
memory = MemoryStore(max_turns=8)

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful Discord assistant. "
    "Be concise, practical, and friendly. "
    "If user asks for code, provide runnable examples."
)

def make_messages(user_id: int, user_text: str):
    system = {"role": "system", "content": DEFAULT_SYSTEM_PROMPT}
    history = memory.get_history(user_id)
    return [system] + history + [{"role": "user", "content": user_text}]

# ====== 슬래시 명령: /chat ======
@tree.command(name="chat", description="LM Studio 로컬 LLM과 대화합니다.")
@app_commands.describe(message="보낼 메시지")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)

    uid = interaction.user.id
    memory.append_user(uid, message)

    try:
        messages = make_messages(uid, message)
        reply = await lm.chat(messages, temperature=0.7, max_tokens=600)
    except Exception as e:
        await interaction.followup.send(f"❌ LM Studio 호출 실패: {e}")
        return

    memory.append_assistant(uid, reply)
    await interaction.followup.send(clamp_discord_message(reply))

# ====== 슬래시 명령: /reset ======
@tree.command(name="reset", description="내 대화 기록(메모리)을 초기화합니다.")
async def reset(interaction: discord.Interaction):
    memory.clear(interaction.user.id)
    await interaction.response.send_message("✅ 대화 메모리를 초기화했어요.", ephemeral=True)

# ====== 슬래시 명령: /ping ======
@tree.command(name="ping", description="봇 상태를 확인합니다.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong ✅", ephemeral=True)

@client.event
async def on_ready():
    # 커맨드 등록(길드 지정 시 즉시 반영)
    if BOT_GUILD_ID != 0:
        guild = discord.Object(id=BOT_GUILD_ID)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
        print(f"Synced commands to guild {BOT_GUILD_ID}")
    else:
        await tree.sync()
        print("Synced commands globally (may take time to appear)")

    print(f"Logged in as {client.user} (id={client.user.id})")
    print(f"LM Studio: {LM_BASE_URL} | model={LM_MODEL}")

def main():
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN이 .env에 없습니다.")
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
