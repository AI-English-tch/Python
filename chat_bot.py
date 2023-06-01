
from GPT import get_completion_from_messages
from config import MAX_SIZE

class ChatBot:
    def __init__(self,context_queue,user_text,event):
        self.context_queue = context_queue
        self.user_text = user_text
        self.event = event
    def chat_bot(self):
        if len(self.context_queue)==1:
            context = list(self.context_queue)  # 将 context_queue 转换为列表
            chat_bot_response = get_completion_from_messages(context)  # 使用 context 而不是 context_queue
            self.context_queue.append({'role': 'assistant', 'content': f"{chat_bot_response}"})
        # self.context_queue.append({'role': 'assistant', 'content': f"{chat_bot_response}"})
        #     yield chat_bot_response,self.context_queue  # 流式输出的核心------
        else:
            self.context_queue.append({'role': 'user', 'content': f"{self.user_text}"})
            chat_bot_response = get_completion_from_messages(list(self.context_queue))  # 使用 context 而不是 context_queue
            self.context_queue.append({'role': 'assistant', 'content': f"{chat_bot_response}"})
            # yield chat_bot_response,self.context_queue  # 流式输出的核心-------
        self.event.set()  # 设置事件，通知 thread_2 可以开始运行
        if len(self.context_queue) >= MAX_SIZE:
            user_or_assistant_count = 0
            count = 0
            while user_or_assistant_count < 2:
                item = self.context_queue[count]
                if item['role'] == 'user' or item['role'] == 'assistant':
                    self.context_queue.remove(item)
                    user_or_assistant_count += 1
                else:
                    count += 1

        return chat_bot_response,self.context_queue

