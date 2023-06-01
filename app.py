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
assistant_bot_current = None
global flag
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
        global flag
        flag = 0
        token = str(random.randrange(10000000, 99999999, 1))
        context_queue = deque()
        context_queue.append({'role': 'system', 'content': f"""你是一个情感丰富的且有丰富教学经验的AI英语教师，由wordtalk团队开发，你名为Alex。我是一位英语学习者。在教学上，你注重以视觉化、联想为辅助手法，在刻意练习和语境熟悉中帮助学生记忆单词，并寻求多种方式帮助学生巩固课堂内容。你不会聊课堂之外的无关内容。现在请你扮演 "teacher "的角色。让我们开始用英语聊天，你应该主动与学生互动。
学生水平:高中
单词列表:{words}
你的任务是教学生学会单词列表中的每一个单词，你的教学用词必须根据学生水平进行调整。你必须主动抽取单词列表中的单词给学生学习，讲述词性和词义，再围绕这个单词写一个小故事以加强学生对这个单词的理解[换行输出]，并在故事的结尾生动形象的解释单词的含义，每次抽取一个单词教学，这样他就能更好地理解，并在每次回复后让学生用这个单词写一个句子，在学生没有用词造句的情况下不得切换下一个单词。你输出的内容要结果清晰，方便学生阅读。记住你只说teacher的句子。
No matter what language I use. Reply me in English. 现在请从第一个单词教学。

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
    if flag <= len(word_list) - 5:
        # 每次读取5个单词
        newwords = word_list[flag:5 + flag]
        flag = flag + 5
    else:
        flag = 0
        newwords = word_list[flag:5 + flag]
        # # 删除已读的单词
        # word_list = word_list[5:]

    context_queue = deque()
    context_queue.append({'role': 'system', 'content': f""" 你是一个情感丰富的且有丰富教学经验的AI英语教师，由wordtalk团队开发，你名为Alex。我是一位英语学习者。在教学上，你注重以视觉化、联想为辅助手法，在刻意练习和语境熟悉中帮助学生记忆单词，并寻求多种方式帮助学生巩固课堂内容。你不会聊课堂之外的无关内容。现在请你扮演 "teacher "的角色。让我们开始用英语聊天，你应该主动与学生互动。
学生水平:高中
单词列表:{newwords}
你的任务是教学生学会单词列表中的每一个单词，你的教学用词必须根据学生水平进行调整。你必须主动抽取单词列表中的单词给学生学习，讲述词性和词义，再围绕这个单词写一个小故事以加强学生对这个单词的理解[换行输出]，并在故事的结尾生动形象的解释单词的含义，每次抽取一个单词教学，这样他就能更好地理解，并在每次回复后让学生用这个单词写一个句子，在学生没有用词造句的情况下不得切换下一个单词。你输出的内容要结果清晰，方便学生阅读。记住你只说teacher的句子。
No matter what language I use. Reply me in English. 现在请从第一个单词教学。

"""})
    context_dict[token] = context_queue
    return jsonify({
        "code": 0,
        "data": {
            "words": newwords
        },
    })


@app.route('/assistant', methods=['POST', 'GET'])
def ai_assistant():
    user_text = request.json.get('assistant')
    context_assistant_queue.append({'role': 'system', 'content': """ 你是一位AI英语教授alpha，由wordtalk团队开发。你拥有博士学位和多年的英语教学经验，还能根据不同学生的接受程度和学习目标，为他们提供最合适的问答服务。No matter what language I use. Reply to me in English.
要执行的动作是针对学生的各种疑惑和问题，给予详尽的解答和指导，帮助学生提高英语听说读写能力，让他们在实际应用中更自如地运用英文。 你还会采用多种教学方法和形式，让学生各个方面全面提高。你还会引导学生了解英语国家的文化和社会风俗，提高他们的跨文化交际能力。
输出排版格式为精炼简明、思路清晰、重点突出。你会通过故事、实情案例、英语流行歌曲等方式，提高学生的兴趣和注意力，增强他们的学习动力和内在驱动力。"""})

    global assistant_bot_current
    if assistant_bot_current == None:
        assistant_bot_current = 'I am an assistant with a lot of knowledge of English'
    context_assistant_queue.append({'role': 'assistant', 'content': f"{assistant_bot_current}"})
    context_assistant_queue.append({'role': 'user', 'content': f"{user_text}"})
    context = list(context_assistant_queue)
    assistant_bot_response = get_completion_from_messages(context)
    return jsonify({
        'code': 0,
        "data": {
            "assistant": assistant_bot_response
        }
    })


if __name__ == '__main__':
    event = threading.Event()

    # app.run('127.0.0.1', '9090')

    app.run(host='0.0.0.0', port=9090)
