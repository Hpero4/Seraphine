
"""
以  #  号分割

1_245_0_0.5268_0.206_0.1178_[876,0.4838&145,0.5351&...]_2#
排名_英雄ID_0_0.胜率_0.ban率_0.登场率_[对位英雄ID,胜率&对位英雄ID,胜率&...]_排名变化#

排名1 艾克(245)
胜率52.68% Ban率20.6% 登场率11.78%
排名变化 +2

"""
import datetime
import re

import requests


class Tencent101:
    def __init__(self):
        self.sess = requests.session()
        tmp = self.sess.get("https://101.qq.com/js/api.js")
        apiJsText = None
        if tmp.status_code == 200:
            apiJsText = tmp.text

        assert apiJsText

        self.rankOverviewUrl = ""
        url_pattern = r'fetchRequest\((`https://[^`]*)\?championid=\$\{heroId\}&lane=\$\{lane\}'
        match = re.search(url_pattern, apiJsText)
        if match:
            self.rankOverviewUrl = match.group(1)

        assert self.rankOverviewUrl


    def get_rank_overview(self, heroId=None, lane=None, ijob=None, gameQueueConfigId=None, tier=None, backDate=None):
        date = backDate if backDate else (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y%m%d')
        heroId = heroId if heroId else '666'
        lane = lane if lane else 'all'
        tier = tier if tier else '200'
        ijob = ijob if ijob else 'all'
        gameQueueConfigId = gameQueueConfigId if gameQueueConfigId else '888'

        url = (f"{self.rankOverviewUrl}?"
               f"championid={heroId}&"
               f"lane={lane}&"
               f"ijob={ijob}&"
               f"dtstatdate={date}&"
               f"gamequeueconfigid={gameQueueConfigId}&"
               f"tier={tier}")
        response = requests.get(url)

        try:
            rs = response.json()
            return rs
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    Tencent101()