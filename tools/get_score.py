import requests
import sys
import json

import openpyxl

import datetime


def read_excel_file(file_path):
    try:
        # Excelファイルを読み込む
        workbook = openpyxl.load_workbook(file_path)
        
        # シートを選択（例: 最初のシートを選択）
        sheet = workbook.active

        # シート内のデータを取得
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        
        return data
    except Exception as e:
        print(f"Excelファイルの読み込みエラー: {str(e)}")
        return None

def main():
    file_path = "../data/Book1.xlsx"  # 読み込むExcelファイルのパスを指定
    excel_data = read_excel_file(file_path)
    get_data = []
    if excel_data:
        # Excelデータを表示
        # print(type(excel_data[0]))
        for row in excel_data:
            print(row)
            if row[1] != None and len(row[1]) >= 1 and row[1] != 'Share it!' and row[1] != 'Participant': 
                get_data.append([row[1][1:],row[10]])

        print(get_data)

        dict_data = dict(get_data)
        print(dict_data)

    with open('../data/get_data.json', 'w') as json_file:
        json.dump(dict_data, json_file, indent=4)
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H%M%S")
    with open('../log/get_data'+timestamp+'.json', 'w') as json_file:
        json.dump(dict_data, json_file, indent=4)
if __name__ == "__main__":
    main()

    