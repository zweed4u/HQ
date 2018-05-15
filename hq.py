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
            'Accept-Encoding':  'gzip, deflate',
            'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-stk':         'MQ==',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'Accept-Language':  'en-us',
            'x-hq-client':      'iOS/1.3.5 b88',
            'x-hq-test-key':    '',
            'Authorization':    f'Bearer {bearer_token}'
        }
        self.my_id = self.get_me()['userId']

    def make_request(self, method, endpoint, params=None, headers=None, payload=None, json=None):
        response = requests.request(method, f'{self.api_base_url}{endpoint}', params=params, headers=headers, data=payload, json=json)
        return response.json()

    def authenticate(self, number):
        headers = {
            'Host':             'api-quiz.hype.space',
            'Content-Type':     'application/json',
            'Accept-Encoding':  'gzip, deflate',
            'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'Accept-Language':  'en-us',
            'x-hq-client':      'iOS/1.3.5 b88',
            'x-hq-test-key':    ''
        }
        json_data = {
            'method': 'sms',
            'phone':  f'+1{number}'
        }
        verification_response = self.make_request('POST', 'verifications', headers=headers, json=json_data)
        self.verification_id = verification_response['verificationId']

        sms_code = input('Enter SMS code sent: ')
        json_data = {
            'code':  sms_code
        }
        verification_sms_response = self.make_request('POST', f'verifications/{verification_id}', headers=headers, json=json_data)
        return verification_sms_response

    def is_username_available(self, desired_username):
        headers = {
            'Host':             'api-quiz.hype.space',
            'Content-Type':     'application/json',
            'Accept-Encoding':  'gzip, deflate',
            'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'Accept-Language':  'en-us',
            'x-hq-client':      'iOS/1.3.5 b88',
            'x-hq-test-key':    ''
        }
        json_data = {
            'username': desired_username
        }
        return self.make_request('POST', 'usernames/available', json=json_data, headers=headers) == {}

    def set_username(self, desired_username):
        if self.is_username_available(desired_username):
            headers = {
                'Host':             'api-quiz.hype.space',
                'Content-Type':     'application/json',
                'Accept-Encoding':  'gzip, deflate',
                'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
                'Connection':       'keep-alive',
                'x-hq-device':      'iPhone6,1',
                'Accept':           '*/*',
                'Accept-Language':  'en-us',
                'x-hq-client':      'iOS/1.3.5 b88',
                'x-hq-test-key':    ''
            }
            json_data = {
                "country": "us",
                "language": "en",
                "locale": "US",
                "username": desired_username,
                "verificationId": self.verification_id
            }
            set_username_response = self.make_request('POST', 'users', json=json_data, headers=headers)
            self.bearer_token = set_username_response['accessToken']
            self.my_id = set_username_response['userId']
        else:
            raise Exception('Username is not available!')

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

    def get_count_of_friend_requests(self):
        return self.make_request('GET', 'friends/requests/incoming/count', headers=self.config_headers)

    def get_friend_requests(self):
        return self.make_request('GET', 'friends/requests/incoming', headers=self.config_headers)

    def friends(self):
        return self.make_request('GET', 'friends', headers=self.config_headers)

    def get_players_from_contacts(self):
        return self.make_request('GET', 'contacts/players', headers=self.config_headers)

    def get_nonplayers_from_contacts(self):
        return self.make_request('GET', 'contacts/non-players', headers=self.config_headers)

    def search_users(self, username_query):
        params = {
            'q': username_query
        }
        return self.make_request('GET', 'users', params=params, headers=self.config_headers)

    def get_user_info(self, user_id):
        return self.make_request('GET', f'users/{user_id}', headers=self.config_headers)

    def get_users_status(self, user_id):
        return self.make_request('GET', f'friends/{user_id}/status', headers=self.config_headers)

    def add_friend(self, user_id):
        headers = {
            'Host':             'api-quiz.hype.space',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'x-hq-client':      'iOS/1.3.5 b88',
            'Authorization':    f'Bearer {self.bearer_token}',
            'Accept-Encoding':  'gzip, deflate',
            'x-hq-stk':         'MQ==',
            'Accept-Language':  'en-us',
            'Content-Type':     'application/json',
            'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-test-key':     ''
        }
        json_data = {}
        return self.make_request('POST', f'friends/{user_id}/requests', json=json_data, headers=headers)

    def block_user(self, user_id):
        headers = {
            'Host':             'api-quiz.hype.space',
            'x-hq-device':      'iPhone6,1',
            'Accept':           '*/*',
            'x-hq-client':      'iOS/1.3.5 b88',
            'Authorization':    f'Bearer {self.bearer_token}',
            'Accept-Encoding':  'gzip, deflate',
            'x-hq-stk':         'MQ==',
            'Accept-Language':  'en-us',
            'Content-Type':     'application/json',
            'User-Agent':       'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
            'Connection':       'keep-alive',
            'x-hq-test-key':     ''
        }
        json_data = {}
        return self.make_request('POST', f'blocks/{user_id}', json=json_data, headers=headers)

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
