import requests

url = 'http://127.0.0.1:5000/repositories'

res = requests.get(url).json()

for repo in res:
    print(repo['rank'])
    print(repo['repositoryName'])
    print(repo['url'])
    print(repo)

