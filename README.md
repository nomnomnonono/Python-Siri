# WhisperとChatGPTを活用したSiri-likeアプリケーション

## 概要
ご自身のPCのマイクから質問すると、Whisperで文字起こしされた質問文がChatGPTに送信されることで回答が得られます。また音声合成ライブラリを活用することで、テキストだけでなく音声の出力も得られます。

Hugging Faceにてアプリケーションを公開しているのでぜひご活用ください。[link](https://huggingface.co/spaces/nomnomnonono/Siri-via-Whisper-ChatGPT)

（OpenAIのAPI keyが必要となります。）

## ローカルでの実行
以下コマンドを実行する。
```bash
# 各種ライブラリインストール
make setup

# gradioの実行
make run
```

## TODO
- 一問一答形式でなく本家のような会話系恣意を実装する
