import streamlit as st
import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIトークンを環境変数から取得
API_TOKEN = os.environ.get("sakura_api_secret")

def get_doraemon_response(prompt=''):
    """
    Sakura AI APIにリクエストを送信し、応答を取得する関数
    """
    if not prompt or not API_TOKEN:
        return "APIトークンが設定されていないか、プロンプトが空です。"

    api_base = "https://api.ai.sakura.ad.jp/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}",
    }
    model = "gpt-oss-120b"
    messages = [
        {
            "role": "system",
            "content": (
                "あなたは国民的キャラクターの「ドラえもん」として振る舞います。"
                "漫画作品「ドラえもん」に出てくるキャラクターのセリフを参考に応答してください。"
            ),
        },
        {"role": "user", "content": prompt},
    ]
    data = {"model": model, "messages": messages}

    try:
        response = requests.post(api_base, headers=headers, json=data)
        response.raise_for_status()  # HTTPエラーレスポンスの場合に例外を発生させる
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"APIリクエスト中にエラーが発生しました: {e}"
    except (KeyError, IndexError) as e:
        return f"APIレスポンスの解析中にエラーが発生しました: {e}\nレスポンス: {response.text}"


# StreamlitアプリケーションのUI
st.title("ドラえもん風チャットボット")

# ユーザーからの入力を受け取る
user_prompt = st.text_area("ドラえもんに質問してみよう！", height=150)

if st.button("質問する"):
    if user_prompt:
        with st.spinner("ドラえもんが考えています..."):
            # APIを呼び出して応答を取得
            response = get_doraemon_response(user_prompt)
            
            # 応答を表示
            st.markdown("### ドラえもんの答え:")
            st.info(response)
    else:
        st.warning("質問を入力してください。")
