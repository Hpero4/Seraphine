import requests
from bs4 import BeautifulSoup


class Opgg:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }

        # Fixme 开启代理时报错
        # Fixme 检测 status 200
        homeHtml = self.sess.get("https://www.op.gg").text
        homeSoup = BeautifulSoup(homeHtml, "lxml")
        self.nextData = homeSoup.find(id="__NEXT_DATA__")



if __name__ == '__main__':
    Opgg()