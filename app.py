import gradio as gr
from utils import answer_by_chat, transcribe

with gr.Blocks() as demo:
    gr.Markdown("Siri-like application via Whisper and ChatGPT")
    with gr.Tabs():
        with gr.TabItem(label="General"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_key = gr.Textbox(label="Paste your own openai-api-key")
                    with gr.Row():
                        audio_input = gr.Audio(
                            source="microphone",
                            type="filepath",
                            label="Record from microphone",
                        )
                        audio_button = gr.Button("Transcribe")
                    audio_output = gr.Textbox()
                with gr.Column(scale=1):
                    chat_button = gr.Button("Questions to ChatGPT")
                    chat_audio_output = gr.Audio()
                    chat_text_output = gr.Textbox()
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
        outputs=[chat_text_output, chat_audio_output],
    )

demo.launch()
