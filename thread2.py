import threading
from assistant_bot import AssistantBot


class Thread2(threading.Thread):
    def __init__(self, user_text,event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_text = user_text
        self.result = None
        self.event = event

    def run(self):
        assistantbot = AssistantBot(self.user_text,event=self.event)
        self.result = assistantbot.assistant_bot()
