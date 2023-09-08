import requests
from requests.exceptions import HTTPError

response = requests.get('https://api.github.com')

if response.status_code == 200:
    print('Success!')
else:
    print('An error occurred!')


for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        # If the response is successful, no Exceptions will be raised
        response.raise_for_status()
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success')