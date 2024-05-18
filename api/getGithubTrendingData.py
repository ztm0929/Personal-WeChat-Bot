import json

import requests

from models import githubTrendingData as github

baseUrl = "https://ghapi.huchen.dev/repositories?language=&since=daily&spoken_language_code=chinese"


def getGithubTrendingData():
    res = requests.get(baseUrl)
    githubTrendingJsonData = res.json()
    githubTrendingData = json.loads(githubTrendingJsonData)

    return github.githubTrendingDataList(githubTrendingData)
