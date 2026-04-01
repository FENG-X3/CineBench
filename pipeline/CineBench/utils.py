import numpy as np
import pandas as pd
import json
import os


def convert_xlsx_to_json(xlsx_path, json_path):
    # 
    if not os.path.exists(xlsx_path):
        print(f"{xlsx_path} not exists")
        return

    df = pd.read_excel(xlsx_path)

    # 
    # df.columns = df.columns.str.lower()

    # N/A None，
    df.replace('N/A', pd.NA, inplace=True)
    df.replace(np.nan, None, inplace=True)

    #  DataFrame 
    data = df.to_dict('records')

    # 
    json_data = []
    for record in data:
        # option1-5candidates
        candidates = []
        for i in range(1, 6):
            option = f'option{i}'
            if option in record and record[option] is not None:
                candidates.append(record[option])
            # option{i}
            record.pop(option, None)
        record['candidates'] = candidates

        # record['correct_choice'] -= 1
        json_data.append(record)

    # json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    xlsx_path = "D:\wxe\HHU\\\CineBench\pipeline\CineBench\data\CineBench_en.xlsx"
    json_path = "D:\wxe\HHU\\\CineBench\pipeline\CineBench\data\cb_en.json"

    convert_xlsx_to_json(xlsx_path, json_path)

    xlsx_path = "D:\wxe\HHU\\\CineBench\pipeline\CineBench\data\CineBench_zh.xlsx"
    json_path = "D:\wxe\HHU\\\CineBench\pipeline\CineBench\data\cb_zh.json"

    convert_xlsx_to_json(xlsx_path, json_path)


    # xlsx_path = "data/Color_en_val.xlsx"
    # json_path = "data/color_en_val.json"
    #
    # convert_xlsx_to_json(xlsx_path, json_path)
    #
    # xlsx_path = "data/Color_zh_val.xlsx"
    # json_path = "data/color_zh_val.json"
    #
    # convert_xlsx_to_json(xlsx_path, json_path)