from scrapy import Request, Spider


def strip(value):
    return value.strip() if isinstance(value, str) else value


class GameStatisticsSpider(Spider):
    name = "game_statistics"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 10))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://www.vgchartz.com/games/games.php?page={i}&order=Sales&ownership=Both&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1")

    def parse(self, response):
            for game in response.xpath(".//div[@id='generalBody']/table/tr"):       
                title = self.get_title(game)
                if title is None:
                    continue  # None-titles are column headers or the footer row
                
                yield {
                    "pos": strip(game.xpath(".//td[1]/text()").get()),
                    "title": title,
                    "platform": strip(game.xpath(".//td[4]/img/@alt").get()),
                    "publisher": strip(game.xpath(".//td[5]/text()").get()),
                    "developer": strip(game.xpath(".//td[6]/text()").get()),
                    "vgchartz_score": strip(game.xpath(".//td[7]/text()").get()),
                    "critic_score": strip(game.xpath(".//td[8]/text()").get()),
                    "user_score": strip(game.xpath(".//td[9]/text()").get()),
                    "total_shipped": strip(game.xpath(".//td[10]/text()").get()),
                    "total_sales": strip(game.xpath(".//td[11]/text()").get()),
                    "na_sales": strip(game.xpath(".//td[12]/text()").get()),
                    "pal_sales": strip(game.xpath(".//td[13]/text()").get()),
                    "japan_sales": strip(game.xpath(".//td[14]/text()").get()),
                    "other_sales": strip(game.xpath(".//td[15]/text()").get()),
                    "release_date": strip(game.xpath(".//td[16]/text()").get()),
                    "last_update": strip(game.xpath(".//td[17]/text()").get()),
                }
 
    def get_title(self, game):
        title = game.xpath(".//td[3]/a/text()").get()
        return title.strip() if isinstance(title, str) else title

