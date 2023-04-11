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
- 英会話の練習ができるようにする
  - GPT4が使えるようになればできそう
  - 使えない場合はシステムメッセージを工夫すればできるかもしれない
    - 入力はWhisperで書き起こされた文章であることを明示して、文章の構造や前後のつながりがおかしい場合は書き起こしのミスを検出、発音の修正までできないか
    - 試した感じだとかなり難しそう
