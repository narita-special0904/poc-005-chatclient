# Azure OpenAI Chat Client (Retry + Timeout + Logging)

## 概要

Azure OpenAIを使用したシンプルなChatクライアントです。
以下の実務機能を実装しています。

* リトライ（Tenacity）
* タイムアウト制御
* ログ出力（logging）
* クラス設計（再利用可能）

---

## 構成

* `LLMClient`

  * Chat API呼び出し
  * リトライ制御
  * エラーハンドリング

---

## セットアップ

### 1. インストール

```
uv pip install -r requirements.txt
```

### 2. 環境変数（.env）

```
AZURE_OPENAI_ENDPOINT=xxx
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_API_VERSION=2024-xx-xx
AZURE_OPENAI_DEPLOYMENT=xxx
```

---

## 実行

```
uv run main.py
```

---

## 主なポイント

### リトライ設計

* RateLimitError
* APIConnectionError
* TimeoutError

に対して最大3回リトライ

---

### タイムアウト

```
timeout=10
```

→ 応答が遅い場合は早期に切断

---

### ログ

```
INFO: 処理開始 / 成功
ERROR: 例外
```

---

## 結果
### 正常時
```text
質問をどうぞ：日本のプロ野球で三冠王獲得者は？
INFO:__main__:処理開始
INFO:__main__:prompt=日本のプロ野球で三冠王獲得者は？...
INFO:__main__:処理成功

日本プロ野球の三冠王（打率・本塁打・打点の同時1位）獲得者は、主に中島治康、野村克也、王貞治、落合博満、松中信彦、村上宗隆などです。特に落合博満は史上唯一の3度達成。セ・パ両リーグで名打者たちが記録してきた、日本球界屈指の偉業です。
```

### タイムアウトリトライ時
```text
質問をどうぞ：日本のプロ野球で三冠王獲得者は？
INFO:__main__:処理開始
INFO:__main__:prompt=日本のプロ野球で三冠王獲得者は？...
INFO:openai._base_client:Retrying request to /chat/completions in 0.427576 seconds
INFO:openai._base_client:Retrying request to /chat/completions in 0.981057 seconds
WARNING:__main__:Retrying __main__.LLMClient._call_api in 1 seconds as it raised APITimeoutError: Request timed out..
INFO:openai._base_client:Retrying request to /chat/completions in 0.474338 seconds
INFO:openai._base_client:Retrying request to /chat/completions in 0.774526 seconds
WARNING:__main__:Retrying __main__.LLMClient._call_api in 1.02 seconds as it raised APITimeoutError: Request timed out..
INFO:openai._base_client:Retrying request to /chat/completions in 0.393055 seconds
INFO:openai._base_client:Retrying request to /chat/completions in 0.788982 seconds
ERROR:__main__:Error!: RetryError[<Future at 0xf3db74769be0 state=finished raised APITimeoutError>]
```

---

## 目的

実務で使える最小構成のAIクライアント実装
