# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import time
import logging

class SingHyPipeline(object):
    csvColumns = ['newsTitle','newsAuthor','newsContent','newsTime','newsType']
    csvContent = []
    csvFileName = []
    def process_item(self, item, spider):
        line = []
        for info in self.csvColumns:
            line.append(item[info])
        # newsTime = item['newsTime'][:4]
        # if newsTime not in self.csvContent.keys():
        #     self.csvContent[newsTime]=[]

        # self.csvContent[newsTime].append(line)
        # if item['newsTime'].find(self.fileName) == -1:
        #     self.saveFile(self.fileName, self.csvContent)
        #     self.fileName = item['newsTime'][:4]
            # self.csvContent.clear()


        self.csvContent.append(line)
        # if len(self.csvContent) % 2000 == 0:
        #     self.saveFile(self.csvContent,str(len(self.csvContent)))
        return item

    def close_spider(self, spider):

        # time.sleep(20)
        self.saveFile(self.csvContent,'2016年')
        # time.sleep(10)



    def saveFile(self,contents,name):
        # for name in contents.keys():
        #     pd.DataFrame(contents[name], columns=self.csvColumns).to_csv('sina行业分析'+ name +'年.csv', encoding='gbk')
        print('开始保存数据.......')
        # time.sleep(25)
        pd.DataFrame(contents, columns=self.csvColumns).to_csv('sina行业分析'+name+'_2.csv', encoding='utf-8')


    def saveList(self,line,contentTime):
        pass


    def logMaster(self,level,msg):
        pass


