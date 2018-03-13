'''自定义爬虫器'''

import scrapy
from scrapy.http import Request,Response
from fundContractPDF.items import FundrawItem
import pandas as pd
import time,csv,numpy,json


class jiasiSpider(scrapy.Spider):
    name = 'jiasiSpider'
    # allowed_domains ='efunds.com.cn'
    # http: // www.jsfund.cn / Services / cn / html / product / gonggao / index.shtml?flag = 7 & fundcode = 070001
    bash_url = 'http://www.jsfund.cn/Services/cn/html/product/gonggao/index.shtml?flag =7&fundcode ='
    start_urls = []
    links = []
    pros = []
    errLink=[]
    i = 0
    j = 0
    # 根据文档获取基金编号
    def getfundId(self):
        file = pd.read_csv("jsfundid.csv", dtype={'Match': str})
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
        # fundIds = ['000005']
        for fund in fundIds:
            baseRefererBeg = 'http://fund.eastmoney.com/f10/jjgg_'
            baseRefererEnd = '_1.html'
            baseurlBeg = 'http://api.fund.eastmoney.com/f10/JJGG?fundcode='
            baseurlEnd = '&pageIndex=1&pageSize=2000&type=1'
            referer = baseRefererBeg + fund + baseRefererEnd
            url = baseurlBeg+ fund +baseurlEnd
            print('准备爬',self.j,referer,url)
            self.j = self.j +1
            yield Request(url,headers={"Referer":referer},callback=self.parse)
            time.sleep(3)




    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        if len(sites['Data']) > 1 :
            site = sites['Data']
        else:
            site = sites['Data'][0]
        id,name = self.getpdfURL(site)
        if id == 'err':
            self.errLink.append()
        base_url = "http://pdf.dfcfw.com/pdf/H2_" + id +"_1.pdf"
        print('正在爬：', self.i,base_url,name)
        self.i = self.i + 1
        item = FundrawItem()
        item['filename'] = name+'.pdf'
        item['file_urls'] = [base_url]
        yield item
        # yield Request(base_url, callback=self.parseD,meta={'name':name})



    def getpdfURL(self,datas):
        for data in datas:
            if data['TITLE'].endswith("基金基金合同") :
                return data['ID'],data['TITLE']
        return 'err'

