import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

class GitHubTrending:
    def __init__(self):
        self.http = self._init_http_session()

    def _init_http_session(self):
        """
        设置重试策略，遇到临时的服务器错误时自动重试，提高代码健壮性和可用性
        """
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        return http
    
    def get_trending_repositories(self):
        """
        获取GitHub Trending的数据并返回格式化的排名信息
        """
        url = 'http://127.0.0.1:5000/repositories'
        res = self.http.get(url).json()

        def format_number(num):
            if num >= 1000:
                return f"{num/1000:.1f}k"
            else:
                return str(num)
        
        formatted_res = []
        for i, repo in enumerate(res):
            if i >= 5:
                break
            repo_info = (
                f"#{repo['rank']} {repo['repositoryName']}\n"
                f"{repo['language']}-{format_number(repo['totalStars'])}-stars⭐\n"
                f"{repo['description']}\n"
                f"{repo['url']}\n"
                f"------"
            )
            formatted_res.append(repo_info)
        
        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

        txt = (
            f"📈 GitHub 每日趋势：\n"
            f"语言-总星数-简介\n\n"
            f"{'\n'.join(formatted_res)}\n\n"
            f"🕒 更新时间：\n"
            f"{datetime_str} UTC+8\n\n"
            f"📊 Data from GitHub\n"
            f"github.com/trending"
        )
        return txt