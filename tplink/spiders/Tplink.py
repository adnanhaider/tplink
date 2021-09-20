import logging
import scrapy
import os
from scrapy import Spider
from tplink.items import Manual


logger = logging.getLogger(__name__)

class Tplink(Spider):
    name = "tplink"
    start_urls = [
        "https://www.tp-link.com/en/choose-your-location/"
        ]

    def parse(self, response):
        urls = response.css('.location-item dd>a::attr(href)').getall()
        for url in urls:
            if url != 'https://www.tp-link.com.cn/':
                url = url+"support/download/"
                yield scrapy.Request(url=url, callback=self.do_parse)
                return
    
    def do_parse(self, response):
        urls = response.css('#list .item .item-box a::attr(href)').getall()
        p_names = response.css('.tp-m-hide::text').getall()
        product_names = ''
        product_name_model_dictionary = {}
        product_container = response.css('.item-box')
        for index, p_name in enumerate(p_names):
            if p_name.count('>') >= 1:
                product_names = (p_name.split('>')[-2].strip() + " " + p_name.split('>')[-1].strip())
            elif(p_name.count('>') == 0 ):
                product_names = p_name.strip()

            models = product_container[index].css('.ga-click::text').getall()
        
            temp_dict = {product_names: models}
            product_name_model_dictionary.update(temp_dict)
        
        for url in urls:
            if not url:
                continue
            if 'http' not in url:
                url = 'https://www.tp-link.com/' + url
            if 'https://static.' in url:
                urls.remove(url)
            if '.zip' in url:
                if url in urls:
                    urls.remove(url)

            yield scrapy.Request(url=url, callback=self.check_version, meta={"dict":product_name_model_dictionary})

    def check_version(self, response):
        dictionary = response.meta.get('dict')

        versions = response.css('.select-version a::attr(href)').getall()

        if len(versions):
            # get pdf for all the versions
            for version_url in versions:
                yield scrapy.Request(url=version_url, callback=self.get_pdf, meta={"dict":dictionary})  
        else:
            yield scrapy.Request(url=response.request.url, callback=self.get_pdf, meta={"dict":dictionary})

    def get_pdf(self, response):
        dictionary = response.meta.get('dict')
        manual = Manual()
        c_url = response.request.url
        lang = c_url.split('/')[3]
        # lang = response.css('html[property="xml:lang"]::text').get()
        pdfs = response.css('.download-list .ga-click::attr(href)').getall()
        if len(pdfs) == 0:
            return
        for pdf in pdfs:
            if ' ' in pdf:
                pdf.replace(' ', '%20')
        
        model = response.css('#model-title-name::text').get()
        thumb = response.css('.product-name img::attr(src)').get()
        product = ''

        for key,value in dictionary.items():
            if model in value:
                product = key
                break
        
        if product:
            manual["product"] = product

        manual["brand"] = 'Tp-link'
        manual["thumb"] = thumb
        manual["model"] = model
        manual["source"] = 'tp-link.com'
        manual["file_urls"] = pdfs
        manual["url"] = c_url
        manual["type"] = response.css('.download-resource .ga-click::text').get().split('_')[-1]
        manual["product_lang"] =  lang 
        # print(manual,'-----------------------------------------------------------')
        return manual