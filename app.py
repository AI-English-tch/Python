from GPT import get_completion_from_messages
from thread1 import Thread1
from thread2 import Thread2
from collections import deque
from config import MAX_SIZE, words
from flask import Flask, request, jsonify, Response
import random
import threading
import os
import tts
os.environ['FLASK_RUN_HOST'] = '23.251.61.213'
os.environ['FLASK_RUN_PORT'] = '9090'

app = Flask(__name__)

# todo：修改为字典
context_dict = dict()
words = ['adequate', 'administrator', 'ally', 'anniversary', 'boundary']
context_assistant_queue = deque()
global assistant_bot_current

# 新的全局变量，包含 50 个六级词汇
word_list = [
        'wisdom', 'allocate', 'determine', 'fabricate', 'narrative',
        'uphold', 'manifest', 'kinetic', 'obsolete', 'venture',
        'zealous', 'quibble', 'paradox', 'illuminate', 'harmony',
        'glimpse', 'evoke', 'juxtapose', 'conviction', 'brisk',
        'affiliate', 'deviate', 'resilience', 'undermine', 'profound',
        'intricate', 'ambiguity', 'epitome', 'confer', 'benevolent',
        'grapple', 'hierarchy', 'inevitable', 'jargon', 'knack',
        'liaison', 'meticulous', 'nostalgia', 'ostracize', 'plausible',
        'qualitative', 'revelation', 'skeptical', 'threshold', 'unprecedented',
        'vulnerable', 'warrant', 'exuberant', 'yield', 'zenith'
    ]


@app.route('/ask', methods=['POST', 'GET'])
# @app.route('http://10.41.136.250/ask', methods=['POST','GET'])
def ai_teacher():  # put application's code here
    try:
        token = request.headers.get('token')

        history_queue = context_dict[token]
        user_text = request.json.get('ask')
        t1 = Thread1(history_queue, user_text, event=event)
        t2 = Thread2(user_text, event=event)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        chat_bot_response = t1.result
        # tts.text_to_audio(text=chat_bot_response)
        context_dict[token] = t1.queue
        assistant_bot_response = t2.result
        global assistant_bot_current
        assistant_bot_current = assistant_bot_response
        # # 前端传输机器人和用户发的言
        # history_queue.append({'role': 'assistant', 'content': f"{chat_bot_response}"})
        # history_queue.append({'role': 'user', 'content': f"{user_text}"})

        # # 更新数据库
        # context_dict[token] = history_queue


        # def generate():
        #
        #     for chat_bot_response_stream in chat_bot_response:
        #         yield jsonify({
        #             "code": 0,
        #             "data": {
        #                 "chat": chat_bot_response_stream,
        #                 "check": assistant_bot_response
        #             }
        #         }) + '\n'  # 首先更新了ai_teacher函数来处理Thread1返回的生成器结果。然后，我将返回值从直接返回一个JSON响应改为返回一个流式响应。在Flask中，可以使用Response对象来创建一个流式响应              Response对象接受一个生成器作为参数，这个生成器在每次有新的数据可供发送时yield数据。在我们的例子中，这个生成器在每次聊天机器人有新的响应时yield一个JSON对象。----------
        #
        # return Response(generate(), mimetype='text/event-stream')


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
    # 第一轮单词
    if token is None:
        token = str(random.randrange(10000000, 99999999, 1))
        context_queue = deque()
        context_queue.append({'role': 'system', 'content': f""" 你是一位有丰富教学经验的英语教师，我是一位英语学习者。现在请你扮演 "teacher "的角色。让我们开始用英语聊天，你应该主动与学生互动。
单词列表:{words}
你的任务是教学生学会单词列表中的每一个单词。你必须主动抽取单词列表中的单词给学生学习，并深入解释单词的含义，每次抽取一个单词教学，这样他就能更好地理解。你非常善于举例说明，并在每次回复后让学生用这个单词写一个句子，在学生没有用词造句的情况下不得切换下一个单词。
在教学过程中，你需要用以下三引号内格式回复并且换行之前末尾加上分号:
'''
Word: 你所回答的问题 ;
Part of speech: 你所回答的问题 ;
explanation: 你所回答的问题 ;
Example sentence: 你所回答的问题 ;
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
    # newwords = ['conspicuous', 'intricate', 'complicated', 'subliminal', 'assistance']
    global word_list
    if len(word_list) > 0:
        # 每次读取5个单词
        newwords = word_list[:5]
        # 删除已读的单词
        word_list = word_list[5:]


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


@app.route('/assistant',methods=['POST','GET'])
def ai_assistant():

    user_text = request.json.get('assistant')
    # context_assistant_queue.append({'role': 'system', 'content': f"{'prompt2'} "})
    global assistant_bot_current

    context_assistant_queue.append({'role': 'assistant', 'content': f"{assistant_bot_current}"})
    context_assistant_queue.append({'role': 'user', 'content': f"{user_text}"})
    context = list(context_assistant_queue)
    assistant_bot_response = get_completion_from_messages(context)
    return jsonify({
        'code':0,
        "data":{
            "assistant":assistant_bot_response
        }
    })


if __name__ == '__main__':

    event = threading.Event()

    # app.run('127.0.0.1', '9090')

    app.run(host='0.0.0.0', port=9090)
