import requests
from getpass import getpass
from requests import models
from requests.auth import HTTPBasicAuth, AuthBase


auth_response = requests.get('http://api.github.com/user', auth= HTTPBasicAuth('username', getpass()))
print(auth_response)


class TokenAuth(AuthBase):
    # implements a custom authentication scheme

    def __init__(self, token):
        self.token = token


    def __call__(self, r):
        # attach api token to a custom auth header 
        r.headers['X-Token'] = f'{self.token}'
        return r
    

response = requests.get('https://httpbin.org/get', auth=TokenAuth('12345abcde-token'))
print(response)