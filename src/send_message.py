import pandas as pd
import random
import time 
import telebot
import threading
import requests
import json
import schedule


f = open("/tmp/config.json")
json = json.load(f)
TOKEN = json["bot-token"]
bot = telebot.TeleBot(TOKEN)
bot_chat_id = json["bot-chat-id"]
time_to_wait_s = json["time-to-wait-s"]
SHEET_ID = json["sheet-id"]
SHEET_NAME = json["sheet-name"]
message_ids = []


def retrieve_data_from_sheet() -> list:
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)
    indx = random.randint(0, len(df))
    target_word = ""
    target_word_hiragana = ""
    target_word_meaning = ""
    for i, row in df.iterrows():
        if(indx == i):
            target_word = row['言葉']
            target_word_hiragana = row['ひらがな']
            target_word_meaning = row['英語の意味']
            break

    message_str_word = "その言葉の意味はなんですか？ \n\n{}".format(target_word)
    message_str_hiraragana = "その言葉のひらがなです： \n\n{}".format(target_word_hiragana)
    message_str_meaning = "その言葉の英語の意味です： \n\n{}".format(target_word_meaning)   
    return [message_str_word, message_str_hiraragana, message_str_meaning]


def send_practice_word() -> None:
    word_list = retrieve_data_from_sheet()
    
    if len(message_ids) > 0:
        for id in message_ids:
            url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={bot_chat_id}&message_id={id}"
            ret = requests.get(url).json() # this sends the message
        
        message_ids.clear()

    for message in word_list:        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={bot_chat_id}&text={message}"
        ret = requests.get(url).json() # this sends the message
        message_ids.append(ret['result']['message_id'])
        time.sleep(time_to_wait_s)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message) -> None:
    bot.reply_to(message, "こんにちは！練習しましょうか？＞.＜")
   

def run_schedule() -> None:
    schedule.every().hour.at(":40").do(send_practice_word)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    polling_thread = threading.Thread(target=bot.infinity_polling, daemon=True)
    scheduling_thread = threading.Thread(target=run_schedule)

    try:
        polling_thread.start()
        scheduling_thread.start()
    except:
        polling_thread.join()
        scheduling_thread.join()