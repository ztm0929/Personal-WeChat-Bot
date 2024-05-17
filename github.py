import requests

req = requests.get('http://0.0.0.0:5000/repositories')

for repo in req.json():
    print(repo['rank'])

