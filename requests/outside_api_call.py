import requests
from requests.exceptions import HTTPError

response = requests.get('https://api.github.com')
print(response.text)
print()
print(response.content)
print()
print(response.headers['content-type'])
print()
print(response.json())

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
        print('Success!')


# search githubs repositoriesfor requests
response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'requests+language:python'},
    headers={'Accept': 'application/vnd.github.v3.text-match+json'},
)

# inspect some attributes of the 'requests' respository
json_response = response.json()
respository = json_response['items'][0]
print(f'Repository name: {respository["name"]}')
print(f'Repository description: {respository["description"]}')  
print(f'Text matches: {respository["text_matches"]}')


bin_response = requests.post('http://httpbin.org/post', json= {'key': 'value'})
json_response = bin_response.json()
print(json_response['data'])
print(json_response['headers']['Content-Type'])
print(bin_response.request.url)
print(bin_response.request.body)