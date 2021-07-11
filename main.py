import csv
import json
from collections import defaultdict
import os
from datetime import datetime, timedelta

import settings
from general_functions import get_messages
from table_generator import Table


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

# get yesterday - start date and today - end date
start_date = datetime.today() - timedelta(days=1)
start_date = str(start_date.combine(start_date.date(), start_date.min.time()).isoformat())

end_date = datetime.today()
end_date = str(end_date.combine(end_date.date(), end_date.min.time()).isoformat())


users = {}
for message in messages:
    # filter messages
    if not message['type'] == 'message' or not start_date <= message['date'] < end_date:
        continue
    # count user messages and chars
    user_id = message['from_id']
    username = message['from']
    text = message['text']
    message_counter[user_id] += 1
    symbol_counter[user_id] += len(text)

    # parse users
    if user_id not in users:
        users[user_id] = username

# count average length of user message
raw_table_data = {}
for user, stats in zip_dict(message_counter, symbol_counter).items():
    avg = round(stats[1]/stats[0], 3)
    raw_table_data[user] = [stats[0], stats[1], avg]

# sort table data for user messages count
raw_table_data = dict(sorted(raw_table_data.items(), key=lambda x: x[1], reverse=True))

# prepare data for csv
raw_csv = []
n = 0
for user_id, values in raw_table_data.items():
    n += 1
    row = {
        '№': n,
        'name': users[user_id],
        'avg_len': '{:6.3f}'.format(values[2]),
        'messages': '{:4d}'.format(values[0]),
        'symbols': '{:5d}'.format(values[1])
    }
    raw_csv.append(row)

headers = list(raw_csv[0].keys())

# replace unsupported chars
for row in raw_csv:
    row['name'] = replace_encoding(row['name'], placeholder='�')

# prepare data for picture table
dataframe = [list(row.values()) for row in raw_csv]

table = Table(headers=headers,
              data=dataframe,
              col_align=['center', 'left', 'center', 'center', 'center']
              )
# table.show()
picture_path = table.save('table.png')
print(picture_path)

# with open('chat_stats.csv', 'w', newline='', encoding='cp1251') as out_file:
#     writer = csv.DictWriter(out_file, delimiter=';', dialect='excel', fieldnames=headers)
#     writer.writeheader()
#     for row in raw_csv:
#         row['name'] = replace_encoding(row['name'])
#     writer.writerows(raw_csv)
#
# os.startfile('chat_stats.csv')

# output_avg = f'{"username":^31} | {"avg_len":^10} | {"messages":^5} | {"symbols":^6}\n'
# output_avg += '\n'.join([f'{str(elem[0]):<31} | {elem[1]:6.4f}' for elem in users_by_avg])
# print(output_avg)
