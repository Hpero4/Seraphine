from app.model.HeroPos import HeroPos
from app.model.RankInfo import RankInfo


class Champion:
    def __init__(self, heroId=None, **kwargs):
        self.heroId = None
        self.rankInfoMap = {
            HeroPos.ALL: None,
            HeroPos.TOP: None,
            HeroPos.JUG: None,
            HeroPos.MID: None,
            HeroPos.BTM: None,
            HeroPos.SUP: None,
        }

        if heroId:
            self.heroId = heroId

        if kwargs.get("data"):
            self.heroId = kwargs["data"].split("_")[1]

        if self.heroId is None:
            raise TypeError("Invalid arguments")

    def __eq__(self, other):
        return self.heroId == other.heroId

    def __add__(self, other):
        """
        当排位信息未加载时, 合并other中的信息

        @param other:
        @return:
        """

        for pos in HeroPos:
            if self.rankInfoMap[pos] is None:
                self.rankInfoMap[pos] = other.rankInfoMap[pos]

        return self
