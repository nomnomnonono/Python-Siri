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


def answer_by_chat(question, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは役に立つアシスタントです。"},
            {"role": "user", "content": question},
        ],
    )
    return response["choices"][0]["message"]["content"]


with gr.Blocks() as demo:
    gr.Markdown("Search fairness paper using this demo.")
    api_key = gr.Textbox(label="Paste your own openai-api-key")
    with gr.Row():
        audio_input = gr.Audio(
            source="microphone", type="filepath", label="Record from microphone"
        )
        audio_button = gr.Button("Transcribe")
    audio_output = gr.Textbox()
    audio_button.click(
        transcribe, inputs=[audio_input], outputs=[audio_output], api_name="transcribe"
    )
    chat_button = gr.Button("Questions to ChatGPT")
    chat_output = gr.Textbox()
    chat_button.click(
        answer_by_chat, inputs=[audio_output, api_key], outputs=[chat_output]
    )
demo.launch()
