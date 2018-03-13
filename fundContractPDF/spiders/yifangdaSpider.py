'''自定义爬虫器'''

import scrapy
from scrapy.http import Request,Response
from fundContractPDF.items import FundrawItem
import pandas as pd
import time,csv,numpy


class yifangdaSpider(scrapy.Spider):
    name = 'yifangdaSpider'
    # allowed_domains ='efunds.com.cn'
    bash_url = 'http://www.efunds.com.cn/html/fund/'
    bashurl = '_lawfile.htm'
    start_urls = []
    links = []
    pros = []
    i = 0
    # 根据文档获取基金编号
    def getfundId(self):
        # file = pd.read_csv("D:\\WorkSpace\\Python\\fundraw\\fundraw\\yfd.csv",dtype={'fundid':str},encoding = "gbk")
        # fundIds = file[['fundid','fundname']]
        file = pd.read_csv("yfdfundid.csv", dtype={'Match': str}, encoding="gbk")
        fundIds = file['Match']
        return numpy.array(fundIds).tolist()

    def writeDataCSV(self,fileName, data):
        out = open(fileName, 'w', newline='')
        csv_writer = csv.writer(out)
        for lineCon in data:
            csv_writer.writerow(lineCon)

    def start_requests(self):
        # 拼接地址
        fundIds = self.getfundId()
        # fundIds = ["000013"]

        for fund in fundIds:
            # url = self.bash_url + fund[0] + self.bashurl
            # yield Request(url, self.parse,meta={'id':fund[0],'name':fund[1]})
            url = self.bash_url + fund + self.bashurl
            yield Request(url, self.parse)
        print('未保存',self.pros)



        # for link in self.links:
        #     print(link)
        #     yield Request(link, self.parseD)
        #     time.sleep(3)
        # yield Request('http://www.23wx.com/quanben/1', self.parse)



    def parse(self, response):
        # self.links.append(response.xpath('//a[contains(text(),"基金合同")]/@href').extract()[0])
        link = response.xpath('//a[contains(text(),"基金合同")]/@href').extract()[0]
        # fundId = response.meta['id']
        # fundname = response.meta['name']
        # yield Request(link, callback=self.parseD,meta={'id':fundId,'name':fundname})
        yield Request(link, callback=self.parseD)


    def parseD(self, response):
        tem = '.pdf'
        item = FundrawItem()
        url = response.xpath('//a[contains(@href,".pdf")]/@href').extract()
        name = response.xpath('//title[contains(text(),"基金")]/text()').extract()
        # name = response.meta['name']
        if len(url) == 0 :
            url = response.xpath('//a[contains(@href,".doc")]/@href').extract()
            tem='.doc'
            # self.pros.append(response)
        print('爬网页：',self.i,url,name)
        self.i = self.i + 1
        # item['filename'] = response.meta['id']+name+tem
        item['filename'] =  name[0][:-6] + tem
        item['file_urls'] = url
        # print('正则爬虫网页',self.i,item['file_url'],item['filename'] )
        yield item