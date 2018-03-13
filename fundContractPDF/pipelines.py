# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
from os.path import basename,dirname,join

class FundContractPDFPipeline(FilesPipeline):

    fileName=''
    def file_path(self, request, response=None, info=None):
        path = join(basename(dirname("/嘉实基金/")), basename(self.fileName))
        return path

    def get_media_requests(self, item, info):
        self.fileName = item['filename']
        for url in item['file_urls']:
            yield scrapy.Request(url)

