import os

import gradio as gr
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=history_openai_format,
        temperature=1.0,
        stream=True,
    )

    partial_message = ""
    try:
        for chunk in iter(response):
            content = chunk.choices[0].delta.content or ""
            if len(content) > 0:
                partial_message = partial_message + content
                yield partial_message
    except TypeError:
        yield ""


demo = gr.ChatInterface(predict)

if __name__ == "__main__":
    demo.queue().launch()
