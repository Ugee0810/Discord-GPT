def clamp_discord_message(text: str, limit: int = 1900) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n…(생략)"
