import csv
import json
from collections import defaultdict
import os
from datetime import datetime

import settings
from general_functions import get_messages


def zip_dict(dict1, dict2):
    out = {}
    for key, val in dict1.items():
        val2 = dict2.get(key)
        out[key] = [val, val2]
    return out


def replace_encoding(text: str, placeholder: str = '') -> str:
    result = ''
    for c in text:
        try:
            c.encode('cp1251')
        except UnicodeEncodeError:
            result += placeholder
        else:
            result += c
    return result


message_counter = defaultdict(int)
symbol_counter = defaultdict(int)

with open(settings.BACKUP_FILE, 'r', encoding='utf-8') as f:
    raw_backup = json.load(f)

messages = get_messages(raw_backup, settings.CHAT_ID)

# get the start of the today in ISO
start_date = datetime.today()
start_date = str(start_date.combine(start_date.date(), start_date.min.time()).isoformat())

for message in messages:
    if not message['type'] == 'message' or message['date'] >= start_date:
        continue
    user_id = message['from_id']
    username = message['from']
    text = message['text']

    message_counter[username] += 1
    symbol_counter[username] += len(text)

avg_lengths = {}
for user, stats in zip_dict(message_counter, symbol_counter).items():
    avg = round(stats[1]/stats[0], 3)
    avg_lengths[user] = [stats[0], stats[1], avg]

avg_lengths = dict(sorted(avg_lengths.items(), key=lambda x: x[1], reverse=True))

raw_csv = []
n = 0
for name, values in avg_lengths.items():
    n += 1
    row = {
        'N': n,
        'name': str(name),
        'avg_len': str(values[2]),
        'messages': values[0],
        'symbols': values[1]}
    raw_csv.append(row)

headers = raw_csv[0].keys()
with open('chat_stats.csv', 'w', newline='', encoding='cp1251') as out_file:
    writer = csv.DictWriter(out_file, delimiter=';', dialect='excel', fieldnames=headers)
    writer.writeheader()
    for row in raw_csv:
        row['name'] = replace_encoding(row['name'])
    writer.writerows(raw_csv)

os.startfile('chat_stats.csv')

# output_avg = f'{"username":^31} | {"avg_len":^10} | {"messages":^5} | {"symbols":^6}\n'
# output_avg += '\n'.join([f'{str(elem[0]):<31} | {elem[1]:6.4f}' for elem in users_by_avg])
# print(output_avg)
