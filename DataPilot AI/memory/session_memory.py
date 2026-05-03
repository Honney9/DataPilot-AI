# memory/session_memory.py

class SessionMemory:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        self.sessions[session_id] = {
            "history": [],
            "state": None  # 🔥 store full pipeline state
        }

    def get(self, session_id):
        return self.sessions.get(session_id)

    def set_state(self, session_id, state):
        if session_id not in self.sessions:
            self.create_session(session_id)

        self.sessions[session_id]["state"] = state

    def get_state(self, session_id):
        session = self.sessions.get(session_id)
        return session.get("state") if session else None

    def append_history(self, session_id, step):
        if session_id not in self.sessions:
            self.create_session(session_id)

        self.sessions[session_id]["history"].append(step)


# 🔥 global instance
memory = SessionMemory()