import threading
from chat_bot import ChatBot


class Thread1(threading.Thread):

    def __init__(self, context_queue, user_text,event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_text = user_text
        self.context_queue = context_queue
        self.result = None
        self.queue = None
        self.event = event

    def run(self):
        chatbot = ChatBot(self.context_queue, self.user_text,self.event)
        for result, queue in chatbot.chat_bot():
            self.result = result
            self.queue = queue
        # self.result,self.queue = chatbot.chat_bot()
        # if self.result:
        #     self.result = list(self.result)  # 使用了list函数将生成器的所有结果保存为一个列表。