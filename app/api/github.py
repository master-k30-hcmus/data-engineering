import requests
from app.config import config


class GithubAPI(object):
    def __init__(self):
        self.token = config.get("GITHUB_TOKEN")

    def get_info(self, repo_name):
        """"""
        headers = {"Authorization": f"token {self.token}"}
        status, headers, data = self._call_api(method='GET', url=f'https://api.github.com/repos/{repo_name}',
                                               headers=headers)
        return data

    def get_repo_feature(self, repo_name, feature):
        """Request api for repository with specific feature

        Params:
          repo_name: name of repository (eg: peng-zhihui/Peak, Chakazul/Lenia)
          feature: in list ('languages', 'contributors', 'tags', 'teams', 'topics', 'events', ...)
        """
        headers = {"Authorization": f"token {self.token}"}
        status, headers, data = self._call_api(method='GET', url=f'https://api.github.com/repos/{repo_name}/{feature}',
                                               headers=headers)
        return (data)

    def _call_api(self, method, url, headers):
        response = requests.request(
            method,
            url,
            headers=headers
        )
        if response.status_code != 200:
            return None, None, None
        else:
            status = response.status_code
            headers = response.headers
            data = response.json()
        return status, headers, data


if __name__ == '__main__':
    api = GithubAPI()
    api.get_info('Chakazul/Lenia')
    feats = ['languages', 'contributors', 'tags', 'teams', 'topics', 'events']
    for feat in feats:
        api.get_repo_feature('Chakazul/Lenia', feat)
