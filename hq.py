#!/usr/bin/python3
import os
import json
import requests
import configparser


class HQ:
    def __init__(self, bearer_token):
        self.config_headers = {
            'Host':             'api-quiz.hype.space',
            'Accept':           '*/*',
            'Connection':       'keep-alive',
            'x-hq-stk':         'MQ==',
            'Accept-Encoding':  'gzip;q=1.0, compress;q=0.5',
            'User-Agent':       'HQ/1.2.19 (co.intermedialabs.hq; build:79; iOS 10.2.0) Alamofire/4.6.0',
            'Accept-Language':  'en-US;q=1.0',
            'Authorization':    f'Bearer {bearer_token}',
            'x-hq-client':      'iOS/1.2.19 b79'
        }
        self.api_base_url = 'https://api-quiz.hype.space/'

    def make_request(self, method, endpoint, params=None, headers=None, payload=None, json=None):
        response = requests.request(method, f'{self.api_base_url}{endpoint}', params=params, headers=headers, data=payload, json=json)
        return response.json()

    def get_config(self):
        config_response = self.make_request('GET', 'config', headers=self.config_headers)
        return config_response

    def get_show_info(self):
        params = {'type': 'hq'}
        show_info_response = self.make_request('GET', 'shows/now', params=params, headers=self.config_headers)
        return show_info_response

    def get_me(self):
        user_response = self.make_request('GET', 'users/me', headers=self.config_headers)
        return user_response


root_directory = os.getcwd()
c = configparser.ConfigParser()
configFilePath = os.path.join(root_directory, 'config.cfg')
c.read(configFilePath)

print(json.dumps(HQ(c.get('authorization', 'token')).get_me(), indent=4))
