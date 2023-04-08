import pandas as pd
import random
import time 
import telebot
import threading
import requests
import json
import schedule
import openai

f = open("/tmp/config.json")
json = json.load(f)
TOKEN = json["bot-token"]
bot = telebot.TeleBot(TOKEN)
bot_chat_id = json["bot-chat-id"]
time_to_wait_s = json["time-to-wait-s"]
SHEET_ID = json["sheet-id"]
SHEET_NAME = json["sheet-name"]
openai.api_key = json["open-api-key"]
message_ids = []

word_rate = 1
MAX_TOKEN_CONFIG = 1000


def get_example_sentence(example_word : str)-> str:
    prompt_text = "Can you give me an example sentence using the following Japanese word '{}'?".format(example_word)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        max_tokens=MAX_TOKEN_CONFIG
    )

    return response.choices[0].text

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
    if len(message_ids) > 0:
        for id in message_ids:
            url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={bot_chat_id}&message_id={id}"
            ret = requests.get(url).json() # this sends the message
        
        message_ids.clear()

    for i in range(word_rate):
        word_list = retrieve_data_from_sheet()
        rei_bun = get_example_sentence(word_list[0])
        word_list.append(rei_bun)
        for message in word_list:        
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={bot_chat_id}&text={message}"
            ret = requests.get(url).json() # this sends the message
            message_ids.append(ret['result']['message_id'])
            time.sleep(time_to_wait_s)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message) -> None:
    bot.reply_to(message, "こんにちは！練習しましょうか？＞.＜")
   
@bot.message_handler(commands=['word'])
def send_welcome(message) -> None:
    bot.reply_to(message, "はい、少々お待ちください。")
    send_practice_word()

@bot.message_handler(commands=['rate'])
def change_message_rate(message) -> None:
    temp_msg = message.text
    temp_msg = temp_msg.replace("/rate ", "")
    
    if temp_msg == "":
        return 
    
    new_rate = int(temp_msg)
    
    if not isinstance(new_rate, int) or new_rate < 1:
        bot.reply_to(message, "申し上げまぜん、｛｝をかえられません".format(new_rate))
        return 
    
    global word_rate
    word_rate = new_rate
    bot.reply_to(message, "私は客先さんのレートを変えていただけませんか？\n新しいレート：{}".format(word_rate))


@bot.message_handler(commands=['reibun'])
def change_message_rate(message) -> None:
    temp_msg = message.text
    example_word = temp_msg.replace("/reibun", "")
    
    if example_word == "":
        return 
    
    rei_bun = get_example_sentence(example_word)
    bot.reply_to(message, rei_bun)


@bot.message_handler(commands=['interval'])
def change_message_rate(message) -> None:
    temp_msg = message.text
    temp_msg = temp_msg.replace("/interval ", "")
    
    if temp_msg == "":
        return 
    
    new_interval = int(temp_msg)
    
    if not isinstance(new_interval, int) or new_interval < 1:
        bot.reply_to(message, "申し上げまぜん、｛｝をかえられません".format(new_interval))
        return 
    
    global time_to_wait_s
    time_to_wait_s = new_interval
    bot.reply_to(message, "私は客先さんのレートを変えていただけませんか？\n新しいレート：{}".format(time_to_wait_s))


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
