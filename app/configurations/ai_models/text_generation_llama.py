import requests
from tokens import URL_SERVER_LLAMA


def generate_answer(messages):
    data = {
        "messages": messages
    }
    response = requests.post(URL_SERVER_LLAMA, json=data)
    answer = response.json().get("response")
    print(answer)
    return answer
