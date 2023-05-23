import openai
openai.api_key = "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"


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
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
