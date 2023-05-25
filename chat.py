from typing import Optional

import numpy as np
import openai
import soundfile
from gtts import gTTS

dic = {"Japanese": "ja", "English": "en"}


class CahtBOT:
    def __init__(self) -> None:
        """初期設定を行う"""
        self.messages = None

    def setup(
        self,
        role1: str,
        content1: str,
        role2: str,
        content2: str,
        role3: str,
        content3: str,
        role4: str,
        content4: str,
        role5: str,
        content5: str,
        api_key: str,
        language: str,
    ) -> None:
        """
        API KEYの登録やプロンプトの初期設定を行う

        Args:
            role1 (str): 1つ目の初期設定プロンプトの役割
            content1 (str): 1つ目の初期設定プロンプト
            role2 (str): 2つ目の初期設定プロンプトの役割
            content2 (str): 2つ目の初期設定プロンプト
            role3 (str): 3つ目の初期設定プロンプトの役割
            content3 (str): 3つ目の初期設定プロンプト
            role4 (str): 4つ目の初期設定プロンプトの役割
            content4 (str): 4つ目の初期設定プロンプト
            role5 (str): 5つ目の初期設定プロンプトの役割
            content5 (str): 5つ目の初期設定プロンプト
            api_key (str): OpenAI API KEY
            language (str): 対象言語
        """

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

    def transcribe(self, audio: tuple[int, np.ndarray]) -> str:
        """
        Whisperによる文字書き起こしを行う

        Args:
            audio (tuple[int, np.ndarray]): 音声データ

        Returns:
            str: 書き起こし文
        """

        sample_rate, data = audio
        soundfile.write(file="tmp.wav", data=data, samplerate=sample_rate)
        audio_file = open("tmp.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text

    def answer_by_chat(
        self, history: list[list[Optional[str]]], question: str
    ) -> list[list[Optional[str]]]:
        """
        ChatGPTによる会話を行う

        Args:
            history (list[list[Optional[str]]]): 今までの会話の履歴
            question (str): 質問文

        Returns:
            list[list[Optional[str]]]: 今回の会話を加えた会話履歴
        """

        self.messages.append({"role": "user", "content": question})
        history += [[question, None]]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        response_text = response["choices"][0]["message"]["content"]
        response_role = response["choices"][0]["message"]["role"]
        response_audio = self.speech_synthesis(response_text)
        self.messages.append({"role": response_role, "content": response_text})
        history += [[None, response_audio]]
        return history

    def speech_synthesis(self, sentence: str) -> str:
        """
        文章を音声ファイルに変換する

        Args:
            sentence (str): 入力文章

        Returns:
            str: 読み上げ音声ファイルパス
        """

        tts = gTTS(sentence, lang=self.language)
        tts.save("tmp.wav")
        return "tmp.wav"
