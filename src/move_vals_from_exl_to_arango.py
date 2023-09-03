import pandas as pd
from arango_handler.arango_handler import Arangohandler, create_database
import argparse
import json 


def retrieve_all_words(sheet_id, sheet_name) -> list:
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    words = []
    for _, row in df.iterrows():
        new_dict = {'言葉': row['言葉'], 'ひらがな': row['ひらがな'], '英語の意味': row['英語の意味']}
        words.append(new_dict)

    return words


def move_words_from_exl_to_arango(sheet_id, sheet_name, arango_handler) -> None:    
    words = retrieve_all_words(sheet_id, sheet_name)
    for word in words:
        arango_handler.insert_row(word)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample file which transfers the legacy google sheets format to the new ArangoDB")

    parser.add_argument("-j", "--path_to_config", type=str, help="The path to the config json file.", required=True)
    parser.add_argument("-c", "--create_db", action='store_true', help="Generate a new DB.", required=False)
    args = parser.parse_args()

    config_path = args.path_to_config
    
    with open(config_path, 'r') as file:
        data = json.load(file)

    if args.create_db:
        username = data["db_username"] 
        password = data["db_password"]
        db_name = data["db_name"]
        create_database(username, password, db_name, "tango")

    handler=Arangohandler(db_name, username, password)
    print("Retrieving words from legacy sheet...")
    move_words_from_exl_to_arango(sheet_name=data["sheet-name"], sheet_id=data["sheet-id"], arango_handler=handler)
    print("repopulation transfer complete, please check new database.")
