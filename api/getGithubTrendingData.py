import requests

from models import githubTrendingData as github

baseUrl = "https://private-anon-e97fe7697c-githubtrendingapi.apiary-mock.com/repositories?language=&since=daily&spoken_language_code=chinese"


def getGithubTrendingData():
    res = requests.get(baseUrl)
    githubTrendingData = res.json()

    return github.githubTrendingDataList(githubTrendingData)
