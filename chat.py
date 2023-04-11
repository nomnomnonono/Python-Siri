import openai
import soundfile

# import whisper
from gtts import gTTS

dic = {"Japanese": "ja", "English": "en"}


class CahtBOT:
    def __init__(self):
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
        language,
    ):
        openai.api_key = api_key
        self.language = dic[language]
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

    def transcribe(self, audio):
        sample_rate, data = audio
        soundfile.write(file="tmp.wav", data=data, samplerate=sample_rate)
        audio_file = open("tmp.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text

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
        tts.save("tmp.wav")
        return "tmp.wav"
