#!/usr/bin/python3
import os
import json
import requests
import configparser


class HQ:
    def __init__(self, phone_number, bearer_token=None):
        self.api_base_url = 'https://api-quiz.hype.space/'
        if bearer_token is None:
            authentication_response = self.authenticate(phone_number)
            bearer_token = authentication_response['auth']['authToken']
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

    def make_request(self, method, endpoint, params=None, headers=None, payload=None, json=None):
        response = requests.request(method, f'{self.api_base_url}{endpoint}', params=params, headers=headers, data=payload, json=json)
        return response.json()

    def authenticate(self, number):
        headers = {
            'Host':             'api-quiz.hype.space',
            'Content-Type':     'application/json',
            'Accept':           '*/*',
            'Connection':       'keep-alive',
            'User-Agent':       'HQ/1.2.19 (co.intermedialabs.hq; build:79; iOS 10.2.0) Alamofire/4.6.0',
            'Accept-Language':  'en-US;q=1.0',
            'x-hq-client':      'iOS/1.2.19 b79',
            'Accept-Encoding':  'gzip;q=1.0, compress;q=0.5'
        }
        json_data = {
            'method': 'sms',
            'phone':  f'+1{number}'
        }
        verification_response = self.make_request('POST', 'verifications', headers=headers, json=json_data)
        verification_id = verification_response['verificationId']

        sms_code = input('Enter SMS code sent: ')
        json_data = {
            'code':  sms_code
        }
        verification_sms_response = self.make_request('POST', f'verifications/{verification_id}', headers=headers, json=json_data)
        return verification_sms_response

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

    def get_leaderboard(self):
        params = {'mode': '1'}
        leaderboard_response = self.make_request('GET', 'users/leaderboard', params=params, headers=self.config_headers)
        return leaderboard_response

    def add_referral_code(self, referringUsername):
        json_data = {'referringUsername': referringUsername}
        referral_response = self.make_request('PATCH', 'users/me', headers=self.config_headers, json=json_data)
        return referral_response


root_directory = os.getcwd()
c = configparser.ConfigParser()
configFilePath = os.path.join(root_directory, 'config.cfg')
c.read(configFilePath)

try:
    bearer_token = c.get('authorization', 'token')
except:
    bearer_token = None
phone_number = str(c.get('verification', 'phone'))
print(json.dumps(HQ(phone_number, bearer_token).get_show_info(), indent=4))
