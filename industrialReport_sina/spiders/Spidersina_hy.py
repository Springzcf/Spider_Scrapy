import scrapy
from industrialReport_sina.items import SingHyItem
from scrapy.http import Request, Response
import time

class sinaHY(scrapy.Spider):
    name = 'industrialReport_sina'
    base = 'http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/industry/index.phtml?p='

    def start_requests(self):
        # for page in range(5355):
        #     url = self.base + page
        #     yield Request(url, callback=self.parse)
        # 拼接地址
        for page in range(915,1700):
        # for page in range(150,160):
        # for page in range(915,950):
            url = self.base + str(page)
            print('开始请求:',url)
            # if page%10 == 0:
            #     time.sleep(10)
            # else:
            time.sleep(3)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        for i in range(3, 43):
            newPathBase = '//table/tr[' + str(i) + ']'
            newsTitle = response.xpath(newPathBase + '/td[2]/a/@title').extract_first()
            newsUrl = response.xpath(newPathBase + '/td[2]/a/@href').extract_first()
            newsTime = response.xpath(newPathBase + '/td[4]/text()').extract_first()
            newsAuthor = response.xpath(newPathBase + '/td[6]/div/span/text()').extract_first()
            print('爬取的信息',newsTitle,newsUrl,newsTime,newsAuthor)
            if newsTime.find('2016') > -1:
                yield Request(newsUrl, callback=self.parseArticle,
                              meta={'title': newsTitle, 'time': newsTime, 'author': newsAuthor})


    def parseArticle(self, response):
        hyItem = SingHyItem()
        hyItem['newsTitle'] = response.meta['title']
        hyItem['newsAuthor'] = response.meta['author']
        hyItem['newsContent'] = self.getContent(response.xpath("//div[@class='blk_container']/p/text()").extract())
        hyItem['newsTime'] = response.meta['time'].strip()
        # hyItem['newsType'] =self.getTypeByTitle(response.meta['title'])
        yield hyItem

    # def getTypeByTitle(self,title):
    #     for type in self.types:
    #         if title.find(type) > -1:
    #             return type

    def getContent(self,contents):
        content =''
        for con in contents:
            con = con.replace('\xa0','').replace(' ','')
            content = content + con
        return content



