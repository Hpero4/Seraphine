class RankInfo:
    def __init__(self, data: str):
        keywords = data.split("_")

        self.index = int(keywords[0])       # 索引
        self.heroId = int(keywords[1])      # 英雄id
        self.priority = int(keywords[2])    # T级
        self.winRate = float(keywords[3])   # 胜率
        self.banRate = float(keywords[4])   # 禁用率
        self.showRate = float(keywords[5])  # 选用率

        # 克制关系(对位时当前英雄的胜率)
        # {英雄ID: 胜率}
        self.restrain = {
            int(key): float(value) for key, value in (
                item.split(",") for item in keywords[6][1:-1].split("&")
            )
        }

        # 最佳搭档(搭配时当前英雄的胜率)
        # {英雄ID: 胜率}
        self.partner = {
            int(key): float(value) for key, value in (
                item.split(",") for item in keywords[7][1:-1].split("&")
            )
        }

        self.rankingChange = int(keywords[8])  # 排名变化
