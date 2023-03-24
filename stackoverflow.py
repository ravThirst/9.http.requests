import requests
from datetime import datetime
from time import sleep
import json


class StackQuestions:
    def __init__(self, tag: str, days: int, key=''):
        self.days = days
        self.now = int(datetime.now().timestamp())
        self.past = self.now - (24 * 60 * 60 * self.days)
        self.url = 'https://api.stackexchange.com/2.3'
        self.key = key.strip()
        self.tag = tag
        self.quota = self.__count_quota()

    def __str__(self):
        res = f'question_tag = {self.tag}\n' \
              f'for_days = {self.days}\n' \
              f'key = {self.key}\n' \
              f'max_quota = {self.quota["quota_max"]}\n' \
              f'remaining = {self.quota["quota_remaining"]}'
        return res

    def __count_quota(self):
        params = {
            'site': 'stackoverflow'
        }
        if self.key:
            params['key'] = self.key

        response = requests.get(f'{self.url}/info', params=params).json()
        return {
            'quota_max': response['quota_max'],
            'quota_remaining': response['quota_remaining']
        }

    def __do_requests(self):
        page_start = 1
        params = {
            'site': 'stackoverflow',
            'fromdate': str(self.past),
            'todate': str(self.now),
            'tagged': self.tag,
            'sort': 'creation',
            'page': page_start,
            'pagesize': 100
        }
        if self.key:
            params['key'] = self.key

        has_more = True
        questions = []

        while has_more:
            response = requests.get(f'{self.url}/questions', params=params)
            for question in response.json()['items']:
                questions.append(question['title'])
            if not response.json()['has_more']:
                has_more = False
            sleep(0.04)
            page_start += 1
            params['page'] = page_start
            self.quota['quota_remaining'] -= 1

        return questions

    @staticmethod
    def __write_json(questions):
        with open('questions.json', 'w') as f:
            data = dict(enumerate(questions, 1))
            json.dump(data, f, ensure_ascii=True, indent=4)

    def get_questions(self):
        print('Please, wait until data is received')
        questions = self.__do_requests()
        self.__write_json(questions)
        print(f'Done!\n'
              f'All questions by tag {self.tag} '
              f'for the last {self.days} day(s)\n'
              f'were dumped into json')
