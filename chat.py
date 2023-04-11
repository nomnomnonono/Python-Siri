import openai
import whisper
from gtts import gTTS


class CahtBOT:
    def __init__(self):
        self.model = whisper.load_model("small")
        self.language = "ja"
        self.messages = None

    def setup(
        self,
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
        self.messages = [
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

    def transcribe(self, filepath):
        audio = whisper.load_audio(filepath)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        self.language = max(probs, key=probs.get)
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(self.model, mel, options)
        return result.text

    def answer_by_chat(self, history, question):
        self.messages.append({"role": "user", "content": question})
        history += [(question, None)]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        response_text = response["choices"][0]["message"]["content"]
        response_role = response["choices"][0]["message"]["role"]
        response_audio = self.speech_synthesis(response_text)
        self.messages.append({"role": response_role, "content": response_text})
        # history += [(None, response_text)]
        history += [(None, (response_audio,))]
        return history

    def speech_synthesis(self, sentence):
        tts = gTTS(sentence, lang=self.language)
        tts.save("tmp.mp3")
        return "tmp.mp3"
