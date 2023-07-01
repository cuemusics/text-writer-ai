

import openai
import pyperclip
import streamlit as st
from audiorecorder import audiorecorder

DEFAULT_MODEL_NAME = "gpt-3.5-turbo-0613"
openai.api_key = "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" # 会社用　

def init_state():
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []
    if "summarize_history" not in st.session_state:
        st.session_state["summarize_history"] = []
    if "title_history" not in st.session_state:
        st.session_state["title_history"] = []
        

def make_return_message():
    init_state()

    if "summarize_history" not in st.session_state:
        message_string = '\n'.join(st.session_state["message_history"])
        summarize_string = '\n'.join(st.session_state["summarize_history"])
        title = st.session_state["title_history"]
        return f"""# {title}

## 要約
{summarize_string}

## 本文
{message_string}"""
    else:
        message_string = '\n'.join(st.session_state["message_history"])
        return f"""{message_string}
"""

def summarize_text_from_text(txt):
    init_state()
    st.session_state["message_history"] = txt
    return summarize_text()

def summarize_text():
        
    def modify_text():
        message_string = '\n'.join(st.session_state["message_history"])

        prompt = f"""# 命令
以下の文章の誤字脱字を修正して、適切に段落をつけてください。
出力は修正後の文章だけにしてください。

# 修正対象の文章
{message_string}

# Output"""
        response =  openai.ChatCompletion.create(
            # model="gpt-3.5-turbo-0613", 
            model="gpt-3.5-turbo-16k",
            # max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
                ]
        )
        assistant_msg = response["choices"][0]["message"]["content"]
        print(assistant_msg)
        st.session_state["message_history"] = assistant_msg.split('\n')
    
    def make_title():
        message_string = '\n'.join(st.session_state["message_history"])

        prompt = f"""# 命令
以下の文章に、全体の内容を分かりやすく表現する適切なタイトル文をつけてください。
タイトル文は20文字以内にしてください。
出力はタイトル文だけにしてください。

# 文章
{message_string}

# Output"""
        response =  openai.ChatCompletion.create(
            # model="gpt-3.5-turbo-0613", 
            model="gpt-3.5-turbo-16k",
            # max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
                ]
        )
        assistant_msg = response["choices"][0]["message"]["content"]
        print(assistant_msg)
        st.session_state["title_history"] = assistant_msg
        print(st.session_state["title_history"])

    init_state()
    modify_text()
    make_title()

    message_string = '\n'.join(st.session_state["message_history"])

    prompt = f"""# 命令
以下の文章を箇条書きで、5行で要約してください。
出力は修正後の文章だけにしてください。

# 要約対象の文章
{message_string}

# Output"""
    response =  openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-0613",  
        model="gpt-3.5-turbo-16k",
        # max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
            ]
    )
    assistant_msg = response["choices"][0]["message"]["content"]
    print(assistant_msg)
    st.session_state["summarize_history"] = assistant_msg.split('\n')

    return make_return_message()

def copy_clipborad(text):
    pyperclip.copy(text)

def transcribe():   
    init_state()
    
    audio_file = open("audio.mp3", "rb")
    transcription = openai.Audio.transcribe("whisper-1", audio_file,language="ja")
    
    st.session_state["message_history"].append(transcription["text"])
    print(transcription["text"])
    # print(message_history.toString())

    return make_return_message()


def main():

    st.title("Text Writer AI")
    audio = audiorecorder("Click to record", "Recording...")
    text_to_display = ""
    if len(audio) > 0:
        # st.audio(audio.tobytes())

        wav_file = open("audio.mp3", "wb")
        wav_file.write(audio.tobytes())
        text_to_display = transcribe()

    if st.button("Summerize"):
        text_to_display = summarize_text()
    
    st.text_area("Text from Sound", value=text_to_display,placeholder="ここに文字起こし結果が出ます",height=500)
if __name__ == "__main__":
    main()