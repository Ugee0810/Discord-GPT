from collections import defaultdict, deque

class MemoryStore:
    def __init__(self, max_turns: int = 8):
        self.max_turns = max_turns
        self._store = defaultdict(lambda: deque(maxlen=max_turns * 2))  # user+assistant 기록

    def append_user(self, user_id: int, content: str):
        self._store[user_id].append({"role": "user", "content": content})

    def append_assistant(self, user_id: int, content: str):
        self._store[user_id].append({"role": "assistant", "content": content})

    def get_history(self, user_id: int):
        return list(self._store[user_id])

    def clear(self, user_id: int):
        self._store[user_id].clear()
