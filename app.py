from thread1 import Thread1
from thread2 import Thread2
from collections import deque
from config import MAX_SIZE, words
from flask import Flask, request, jsonify
import random
import threading
import os

os.environ['FLASK_RUN_HOST'] = '23.251.61.213'
os.environ['FLASK_RUN_PORT'] = '9090'

app = Flask(__name__)

# todo：修改为字典
context_dict = dict()
words = ['adequate', 'administrator', 'ally', 'anniversary', 'boundary']


@app.route('/ask', methods=['POST', 'GET'])
# @app.route('http://10.41.136.250/ask', methods=['POST','GET'])
def ai_teacher():  # put application's code here
    try:
        token = request.headers.get('token')
        # if token is None:
        #     token = str(random.randrange(10000000,99999999,1))
        #     context_queue = deque()
        #     context_queue.append({'role': 'system', 'content': f""" 你是一位友好主动的英语教师，我是一位英语学习者。\
        #           现在请你扮演 "teacher "的角色，我将扮演 "student "的角色。\
        #           让我们开始用英语聊天，你应该主动与学生互动。\
        #           请设置上下文的对话，这样我就能更容易地理解和记住这些单词。\
        #           我们将进行多轮对话，每轮只需要教学生一个单词，这样他就能更好地理解。\
        #           你一次只应该展示一轮对话中teacher的句子，其他的不要输出。现在让我们以下面这句话开始： \
        #           "student: Hello teacher, today I want to learn these word :{words}。\
        #           "请在句子中突出你想学的单词,记住你只能说英文,在你的每一次对话的最后你都需要让学生用这个单词写一个句子，记住你只说teacher的句子。 记住你只说teacher的句子"""})
        #     context_dict[token] = context_queue
        #     return jsonify({
        #         "code": 0,
        #         "data": {
        #             "token": token
        #         },
        #     })
        history_queue = context_dict[token]
        user_text = request.json.get('ask')
        event = threading.Event()
        print(event)
        t1 = Thread1(history_queue, user_text, event=event)
        t2 = Thread2(user_text, event=event)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        chat_bot_response = t1.result
        context_dict[token] = t1.queue
        assistant_bot_response = t2.result
        # # 前端传输机器人和用户发的言
        # history_queue.append({'role': 'assistant', 'content': f"{chat_bot_response}"})
        # history_queue.append({'role': 'user', 'content': f"{user_text}"})

        # # 更新数据库
        # context_dict[token] = history_queue

        return jsonify({
            "code": 0,
            "data": {
                "chat": chat_bot_response,
                "check": assistant_bot_response
            }
        })

    except Exception as e:
        return jsonify({
            "code": 1,
            "data": str(e)
        })


@app.route('/word', methods=['POST', 'GET'])
def ai_word():
    # words = request.data.word
    token = request.headers.get('token')
    print(token)
    # 第一轮单词
    if token is None:
        token = str(random.randrange(10000000, 99999999, 1))
        context_queue = deque()
        context_queue.append({'role': 'system', 'content': f""" 你是一位有丰富教学经验的英语教师，我是一位英语学习者。现在请你扮演 "teacher "的角色。让我们开始用英语聊天，你应该主动与学生互动。
单词列表:{word}
你的任务是教学生学会单词列表中的每一个单词。你必须主动抽取单词列表中的单词给学生学习，并深入解释单词的含义，每次抽取一个单词教学，这样他就能更好地理解。你非常善于举例说明，并在每次回复后让学生用这个单词写一个句子，在学生没有用词造句的情况下不得切换下一个单词。
在教学过程中，你需要用以下三引号内格式回复:
'''
Word:
Part of speech:
explanation:
Example sentence:
can you give me a sentence use <word>
'''
No matter what language I use.Reply me in English.现在请从第一个单词教学。
"""})
        context_dict[token] = context_queue
        return jsonify({
            "code": 0,
            "data": {
                "token": token,
                "words": words
            },
        })

    # 第二轮单词
    newwords = ['conspicuous', 'intricate', 'complicated', 'subliminal', 'assistance']
    context_queue = deque()
    context_queue.append({'role': 'system', 'content': f""" 你是一位友好主动的英语教师，我是一位英语学习者。\
                          现在请你扮演 "teacher "的角色，我将扮演 "student "的角色。\
                          让我们开始用英语聊天，你应该主动与学生互动。\
                          请设置上下文的对话，这样我就能更容易地理解和记住这些单词。\
                          我们将进行多轮对话，每轮只需要教学生一个单词，这样他就能更好地理解。\
                          你一次只应该展示一轮对话中teacher的句子，其他的不要输出。现在让我们以下面这句话开始： \
                          "student: Hello teacher, today I want to learn these word :{newwords}。\
                          "请在句子中突出你想学的单词,记住你只能说英文,在你的每一次对话的最后你都需要让学生用这个单词写一个句子，记住你只说teacher的句子。 记住你只说teacher的句子"""})
    context_dict[token] = context_queue
    return jsonify({
        "code": 0,
        "data": {
            "words": newwords
        },
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
