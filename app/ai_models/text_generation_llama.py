from huggingface_hub import InferenceClient

from tokens import LLAMA_TOKEN

client = InferenceClient(api_key=LLAMA_TOKEN)


def generate_answer(messages, answer=None):
    if answer is None:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=messages,
            max_tokens=256,
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0.5
        )
        response = completion.choices[0].message["content"]
    else:
        response = answer
    return response
