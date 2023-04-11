import gradio as gr
from chat import CahtBOT

chat = CahtBOT()


with gr.Blocks() as demo:
    gr.Markdown("Siri-like application via Whisper and ChatGPT")
    with gr.Tabs():
        with gr.TabItem(label="General"):
            with gr.Row():
                with gr.Column(scale=1):
                    api_key = gr.Textbox(label="Paste your own openai-api-key")
                    api_button = gr.Button("SetUp")
                    with gr.Row():
                        audio_input = gr.Audio(
                            source="microphone",
                            label="Record from microphone",
                        )
                        audio_button = gr.Button("Transcribe")
                    audio_output = gr.Textbox()
                    chat_button = gr.Button("Questions to ChatGPT")
                with gr.Column(scale=1):
                    chatbot = gr.Chatbot([], elemid="chatbot").style(height=750)
        with gr.TabItem(label="Setting"):
            gr.Markdown("Prompt Setting")
            language = gr.Dropdown(["Japanese", "English"], value="English")
            with gr.Row():
                role1 = gr.Dropdown(["system", "user", "assistant"], value="system")
                content1 = gr.Textbox(value="You're helpful assistant.")
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

    api_button.click(
        chat.setup,
        inputs=[
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
            language,
        ],
        outputs=None,
    )
    audio_button.click(
        chat.transcribe,
        inputs=[audio_input],
        outputs=[audio_output],
        api_name="transcribe",
    )
    chat_button.click(
        chat.answer_by_chat,
        inputs=[chatbot, audio_output],
        outputs=[chatbot],
    )

demo.launch()
