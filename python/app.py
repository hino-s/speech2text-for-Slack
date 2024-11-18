import os
import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI
import threading

print("Starting app.py")  # for debug
load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"], process_before_response=True)
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def process_audio(event, say):
    if not ("files" in event):
        output = "ファイルが見つかりません。\n対応するファイルは以下の通りです。\nmp3, mp4, mpeg, mpga, m4a, wav, webm"
    else:
        file = event["files"][0]
        filetype = file["filetype"]
        
        if filetype in ["mp3", "mp4", "mpeg", "m4a", "mpga", "webm", "wav"]:
            title = file["title"]
            url = file["url_private"]
            extension = os.path.splitext(url)[1]
            filename = "tmp" + extension
            resp = requests.get(url, headers={'Authorization': 'Bearer %s' % os.environ["SLACK_BOT_TOKEN"]})
            with open(filename, 'wb') as f:
                f.write(resp.content)
                thread_ts = event.get("thread_ts") or None
                channel = event["channel"]
                if thread_ts is not None:
                    say(text="読み込み中．．．", thread_ts=thread_ts, channel=channel)
                else:
                    say(text="読み込み中．．．", channel=channel)
            if os.path.getsize(filename) > 25000000:              
                output = "ファイルサイズオーバー。ファイルサイズは25MB以下に分割してください"
            else:
                if os.path.getsize(filename) > 12000000:
                    say(text="ファイルサイズが大きいため，処理に時間がかかることが予想されます",  channel=channel)
                with open(filename, "rb") as audio_file:
                    language = "ja"
                    print(audio_file)
                    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language=language)
                    organized_text = organize_text_by_speaker(transcript.text)
                output = f"書き起こし完了：{title}\n----\n" + organized_text
            os.remove(filename)
        else:
            output = "対応するファイルではありません。対応するファイルは以下の通りです。\nmp3, mp4, mpeg, mpga, m4a, wav, webm"
    
    # スレッド内でsayを呼び出して応答を送信
    thread_ts = event.get("thread_ts") or None
    channel = event["channel"]
    if thread_ts is not None:
        say(text=output, thread_ts=thread_ts, channel=channel)
    else:
        say(text=output, channel=channel)
    print(output)

@app.event("message")
def handle_message(event, say, ack):
    ack()  # すぐに応答してSlackの3秒制限を回避
    # 非同期で音声処理を実行
    threading.Thread(target=process_audio, args=(event, say)).start()

def organize_text_by_speaker(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "音声認識のテキストを話者ごとに段落分けして整理してください。またテキストが長くない場合などの登場人物が一人のみの場合，見やすく段落分けするだけで結構です．テキストの文字を絶対に変更せずに段落分けのみしてください"},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    organized_text = response.choices[0].message.content
    return organized_text

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()