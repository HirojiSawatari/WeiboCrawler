# -*- coding: gb2312 -*-

'''
Created on 2017-03-02

@author: Sawatari
'''

import sys
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from WeiboCrawler.items import WeibocrawlerItem

class WeiboCrawler(Spider):
    name = "WeiboCrawler"
    download_delay = 4
    allowed_domains = ["weibo.cn"]
    start_urls = [
        "http://weibo.cn/"
    ]

    def parse(self, response):
        # 反复确认是否搜索成功
        if response.url == "http://weibo.cn/":
            # 读取临时文件
            temp = open('tempkey.temp', 'r')
            keyword = temp.read()
            temp.close()
            # 搜索关键词第一页
            url = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + "&page=1"
            # 将中文转码为uft-8
            url = url.decode("GBK").encode("utf-8")
            # 递归
            yield Request(url, callback=self.parse)

        else:
            # 搜索成功
            item = WeibocrawlerItem()
            sel = Selector(response)
            results = sel.xpath('//*[@class="c"]')
            for result in results:
                name = result.xpath('div/span[@class="ctt"]/text()').extract()

                # sys.getfilesystemencoding()获得本地编码（mbcs编码）
                item['name'] = [na.encode(sys.getfilesystemencoding()) for na in name]
                yield(item)
            # 提取关键词
            keyword = response.url[(response.url.index("keyword=") + 8):response.url.index("&page")]
            # 递归
            next_page_urls = []
            # 500页列表
            for i in range(2, 100, 1):
                page = str(i)
                next_page_urls.append("http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + "&page=" + page)
            # 递归获取后页
            for next_page_url in next_page_urls:
                yield Request(next_page_url, callback=self.parse)