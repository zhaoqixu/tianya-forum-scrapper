#!/usr/bin/python

import scrapy


class CorpusSpider(scrapy.Spider):
    name = "corpus"

    def start_requests(self):
        urls = [
            'http://bbs.tianya.cn/post-house-730908-1.shtml',
            'http://bbs.tianya.cn/post-934-162415-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1804443-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1803949-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1689181-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1804001-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1531237-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-1804649-1.shtml',
            'http://bbs.tianya.cn/post-worldlook-358684-1.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for corpus in response.css('div.atl-item'):
            yield {    
                'text': corpus.css('div.bbs-content::text').extract_first(),
                'hostid': corpus.css('div.atl-info a::attr(uid)').extract_first(),
                'reply': corpus.css('span.ir-content::text').extract(),
                'guestid': corpus.css('li::attr(_userid)').extract(),
            }

        next_page = response.css('a.js-keyboard-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


