from GPT import get_completion
from config import context_number


class AssistantBot:
    def __init__(self, user_text,event):
        self.user_text = user_text
        self.event = event
        self.context_number = context_number

    def assistant_bot(self):
        self.event.wait()
        if self.user_text:
            context2 = f"""please think step by step:Check the sentences in <> for misspellings or grammatical errors, and if so, point them out and correct them.<{self.user_text}>"""
            assistant_bot_response = get_completion(context2)
            return assistant_bot_response
        print("!213123")
        return None
