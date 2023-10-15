
"""
以  #  号分割

1_245_0_0.5268_0.206_0.1178_[876,0.4838&145,0.5351&...]_2#
排名_英雄ID_0_0.胜率_0.ban率_0.登场率_[对位英雄ID,胜率&对位英雄ID,胜率&...]_排名变化#

排名1 艾克(245)
胜率52.68% Ban率20.6% 登场率11.78%
排名变化 +2

"""
import datetime
import json
import re

import requests

from app.model.Champion import Champion
from app.model.HeroPos import HeroPos
from app.model.RankInfo import RankInfo


class Tencent101:
    def __init__(self):
        self.sess = requests.session()
        self.championMap = {}

        # 排行概述, 只保存 championId, 排序按照T级
        self.rankOverview = {
            HeroPos.TOP: [],
            HeroPos.JUG: [],
            HeroPos.MID: [],
            HeroPos.BTM: [],
            HeroPos.SUP: [],
            HeroPos.ALL: [],
        }

        tmp = self.sess.get("https://101.qq.com/js/api.js")
        apiJsText = None
        if tmp.status_code == 200:
            apiJsText = tmp.text

        assert apiJsText

        self.rankOverviewUrl = ""
        url_pattern = r'fetchRequest\(`(https://[^`]*)\?championid=\$\{heroId\}&lane=\$\{lane\}'
        match = re.search(url_pattern, apiJsText)
        if match:
            self.rankOverviewUrl = match.group(1)

        assert self.rankOverviewUrl

        for pos in HeroPos:
            rankOverviewData = self.getRankOverview(lane=pos)
            self.loadRankOverview(rankOverviewData, pos)

        print()

    def getRankOverview(self, heroId=None, lane: HeroPos=None, ijob=None, gameQueueConfigId=None, tier=None, backDate=None):
        """
        字段	类型	字段描述	字段意义
        dtstatdate	string	日期	例如：20210517
        championid	string	英雄ID	666：所有英雄
        gamequeueconfigid	string	模式	420：单双排，440：灵活组排，450：大乱斗，700：冠军杯赛，888：所有模式
        tier	bigint	段位	"段位区间:
        0:王者 ，5：宗师，6：大师，10：钻石，20：铂金，30：黄金，40：白银，50：黄铜，80：黑铁
        200：铂金以上
        311：峡谷之巅铂金以上"
        lane	string	位置	all：所有位置
        ijob	string	英雄职业	all：所有职业
        championdetails	string	英雄详情

        英雄详情：每个英雄信息用#隔开，
        单个英雄详细信息用_隔开，从左到右分别是排名，英雄id、级别、胜率、禁用率、选率、英雄克制详情、最佳双排详情；
        级别：0~4
        0：T0，1：T1，2：T2，3：T3，4：T4；
        英雄克制详情：整个信息放到[]中；克制英雄id和胜率之间用英文逗号,分隔；每个克制英雄信息之间用&隔开；若英雄克制详情为空则返回[]；
        如：[64,0.6667&80,1.0]
        其中64和80是克制英雄id，0.6667和1.0是克制胜率；
        最佳双排详情：整个信息放到[]中；英雄id和双排胜率之间用英文逗号,分隔；每个双排英雄信息之间用&隔开；若英雄最佳双排TOP3详情为空则返回[]；
        如：[99,0.6061&141,0.5714&245,0.5595]
        其中99、141、245是最佳双排前三的英雄id，0.6061、0.5714、0.5595分别是TOP3的双排胜率"

        """
        date = backDate if backDate else (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y%m%d')
        heroId = heroId if heroId else '666'
        lane = lane.value if lane else 'all'
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

            assert rs.get("HttpStatus") == 200

            return json.loads(rs["data"]["result"])["championdetails"]
        except Exception as e:
            return str(e)

    def loadRankOverview(self, data: str, pos: HeroPos):
        for championData in data.split("#"):
            champion = Champion(data=championData)

            self.rankOverview[pos].append(champion.heroId)
            champion.rankInfoMap[pos] = RankInfo(championData)

            if champion.heroId in self.championMap:
                self.championMap[champion.heroId] += champion
            else:
                self.championMap[champion.heroId] = champion



if __name__ == '__main__':
    print("start")
    Tencent101()
