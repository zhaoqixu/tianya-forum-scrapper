# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#coding=UTF-8
import re

class CorpusPipeline(object):
	def open_spider(self, spider):
		self.file = open('corpus_ty.xml','a+')

	def process_item(self, item, spider):
		if item['guestid'] == []:
			return
		
		k = 2
		dict = {item['hostid']: 1}

		for id in item['guestid']:
			if id not in dict:
				dict[id] = k
				k+=1

		text = re.sub('\s+', '', item['text'])
		self.file.write("\t<s>\n")
		self.file.write("\t\t<utt uid=\"{0}\">{1}</utt>\n".format(1, text))
		i = 0
		for r in item['reply']:
			if r == u'评论 ':
				item['reply'].remove(r)
		for reply in item['reply']:
			reply = re.sub('\s+', '', reply)
			reply = re.sub(r'.*：', '', reply)
			self.file.write("\t\t<utt uid=\"{0}\">{1}</utt>\n".format(dict[item['guestid'][i]], reply))
			i += 1
		self.file.write("\t</s>\n")
		return item


	def close_spider(self, spider):
		self.file.close()