import gradio as gr
import openai
import whisper

model = whisper.load_model("small")


def transcribe(filepath):
    audio = whisper.load_audio(filepath)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    return result.text


def answer_by_chat(
    question,
    role1,
    content1,
    role2,
    content2,
    role3,
    content3,
    role4,
    content4,
    role5,
    content5,
    api_key,
):
    openai.api_key = api_key
    messages = [
        {"role": role, "content": content}
        for role, content in [
            [role1, content1],
            [role2, content2],
            [role3, content3],
            [role4, content4],
            [role5, content5],
        ]
        if role != "" and content != ""
    ]
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response["choices"][0]["message"]["content"]


with gr.Blocks() as demo:
    gr.Markdown("Siri-like application via Whisper and ChatGPT")
    with gr.Tabs():
        with gr.TabItem(label="General"):
            api_key = gr.Textbox(label="Paste your own openai-api-key")
            with gr.Row():
                audio_input = gr.Audio(
                    source="microphone", type="filepath", label="Record from microphone"
                )
                audio_button = gr.Button("Transcribe")
            audio_output = gr.Textbox()
            chat_button = gr.Button("Questions to ChatGPT")
            chat_output = gr.Textbox()
        with gr.TabItem(label="Setting"):
            gr.Markdown("Prompt Setting")
            with gr.Row():
                role1 = gr.Dropdown(["system", "user", "assistant"], value="system")
                content1 = gr.Textbox(value="あなたは役に立つアシスタントです。")
            with gr.Row():
                role2 = gr.Dropdown(["system", "user", "assistant"])
                content2 = gr.Textbox()
            with gr.Row():
                role3 = gr.Dropdown(["system", "user", "assistant"])
                content3 = gr.Textbox()
            with gr.Row():
                role4 = gr.Dropdown(["system", "user", "assistant"])
                content4 = gr.Textbox()
            with gr.Row():
                role5 = gr.Dropdown(["system", "user", "assistant"])
                content5 = gr.Textbox()
    audio_button.click(
        transcribe, inputs=[audio_input], outputs=[audio_output], api_name="transcribe"
    )
    chat_button.click(
        answer_by_chat,
        inputs=[
            audio_output,
            role1,
            content1,
            role2,
            content2,
            role3,
            content3,
            role4,
            content4,
            role5,
            content5,
            api_key,
        ],
        outputs=[chat_output],
    )
demo.launch()
