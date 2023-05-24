from GPT import get_completion_from_messages
from config import context_number


class AssistantBot:
    def __init__(self, user_text, event):
        self.user_text = user_text
        self.event = event
        self.context_number = context_number

    def assistant_bot(self):
        self.event.wait()
        if self.user_text:
            context2 = {'role': 'system', 'content': f"""你是一位英语助理教授，你拥有着及其刁钻的眼光，对于语法、词汇等错误有极高的敏感度。现在请你扮演英语助理教授的角色。No matter what language I use.Reply me in English.
你的任务是分析学生提交给你的句子，如果是英文就加以纠错和点评，你所举例的句子必须足够口语化，像native speaker一样，如果是中文就翻译为英文并放在"Original sentence:"栏目中。学生的句子：{self.user_text}。
'''
Original sentence:
Grammatical errors:
Spelling mistakes:
Corrected sentence.:
More synonymous sentences:
"""}
            assistant_bot_response = get_completion_from_messages(context2)
            return assistant_bot_response
        print("!213123")
        return None
