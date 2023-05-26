import openai
openai.api_key = "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"


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
        temperature=0,
    )
    return response.choices[0].text

def get_text_to_speech(text):
    response = openai.Completion.create(
        engine = "dall-e-2-musk",
        prompt = f"convert the following text to speech: {text}",
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.7
    )
    return response.choices[0].audio_content
