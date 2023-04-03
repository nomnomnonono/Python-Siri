import openai
import whisper
from gtts import gTTS

model = whisper.load_model("small")


def transcribe(filepath):
    audio = whisper.load_audio(filepath)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    global language
    language = max(probs, key=probs.get)
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
    response_text = response["choices"][0]["message"]["content"]
    response_audio = speech_synthesis(response_text)
    return response_text, response_audio


def speech_synthesis(sentence):
    tts = gTTS(sentence, lang=language)
    tts.save("tmp.mp3")
    return "tmp.mp3"
