import pywhatkit
import pandas as pd
import random

def send_message():
    SHEET_ID = '1McY4ryAWgUACggAcNh0Gpv3hlz4fc9mKJqDMFkt2k70'
    SHEET_NAME = 'japanese'
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

    message_str = "その言葉の意味はなんですか？ \n{}".format(target_word)
    pywhatkit.sendwhatmsg_instantly("+447548911979", message_str, wait_time=5, tab_close=True, close_time=3)

if __name__ == "__main__":
    print("hello.\n")
    send_message()
    