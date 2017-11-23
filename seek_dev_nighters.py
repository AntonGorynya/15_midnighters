import requests
import pytz
import datetime
import pprint


URL = 'http://devman.org/api/challenges/solution_attempts/'
MORNING_HOUR = 7


def load_attempts():
    param = {'page': 1}
    response = requests.get(URL, params=param).json()
    number_of_pages = response['number_of_pages']
    users_info = response['records']
    for page in range(2, number_of_pages + 1):
        users_info += requests.get(URL,
                                   params={'page': page}).json()['records']
    return users_info


def get_midnighters(users_info):
    midnighters = {}
    for record in users_info:
        user = record['username']
        local_time_zone = pytz.timezone(record['timezone'])
        local_time = pytz.utc.localize(
            datetime.datetime.fromtimestamp(record['timestamp']))
        local_time.astimezone(local_time_zone)
        if local_time.hour < MORNING_HOUR:
            if user in midnighters:
                midnighters[user].append(local_time)
            else:
                midnighters.update({user: [local_time]})
    return midnighters


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    for user_data in midnighters:
        print('{} send:'.format(user_data))
        for send_time in midnighters[user_data]:
            print('{:>10}'.format(send_time.strftime('%H:%M:%S')))
