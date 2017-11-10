import requests
import pytz
import datetime


URL = 'http://devman.org/api/challenges/solution_attempts/?page={}'
MORNING_HOUR = 7


def load_attempts():
    pages = 1
    responce = requests.get(URL.format(pages)).json()
    number_of_pages = responce['number_of_pages']
    records = responce['records']
    records = records+([requests.get(URL.format(page)).json()['records']
                        for page in range(2, number_of_pages+1)][0])
    return records


def get_midnighters(records):
    midnighters = {}
    for record in records:
        user = record['username']
        local_time_zone = pytz.timezone(record['timezone'])
        local_time = pytz.utc.localize(
            datetime.datetime.fromtimestamp(record['timestamp']))
        local_time.astimezone(local_time_zone)
        if local_time.hour < MORNING_HOUR:
            midnighters.update(zip([user], [local_time.strftime('%H:%M:%S')]))
    return midnighters


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    for user_name in midnighters:
        print('{} send {}'.format(user_name, midnighters[user_name]))
