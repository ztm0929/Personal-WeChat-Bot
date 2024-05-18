class githubTrendingDataList:
    def __init__(self, list):
        self.list = list

        for index, item in enumerate(self.list):
            self.list[index] = githubTrendingData(item['author'], item['name'], item['url'], item['description'],
                                                  item['language'], item['stars'], item['forks'],
                                                  item['currentPeriodStars'])


class githubTrendingData:
    def __init__(self, author, name, url, description, language, stars, forks, starsToday):
        self.author = author
        self.name = name
        self.url = url
        self.description = description
        self.language = language
        self.stars = stars
        self.forks = forks
        self.starsToday = starsToday
