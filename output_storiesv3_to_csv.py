import csv
import json

# JSONファイルからデータを読み込む
with open("output_storiesv3.json", 'r') as f:
    data = json.load(f)

# CSVファイルに書き込む
with open("output_storiesv3.csv", 'w', newline='') as f:
    writer = csv.writer(f)

    # ヘッダーを書き込む (最初の要素のキーをヘッダーとして使用)
    if data:
        header = data[0].keys()
        writer.writerow(header)

        # データを書き込む
        for row in data:
            writer.writerow(row.values())
