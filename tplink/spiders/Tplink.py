import logging
import scrapy
import os
from scrapy import Spider
# from vandenborre.items import Manual


logger = logging.getLogger(__name__)

class Tplink(Spider):
    name = "tplink"
    start_urls = [
        "https://www.tp-link.com/en/support/download/"
        ]
    
    def parse(self, response):
        urls = response.css('#list .item .item-box a::attr(href)').getall()
        for url in urls:
            if not url:
                continue
            if 'http' not in url:
                url = 'https://www.tp-link.com/' + url
            if 'https://static.' in url or '.zip' in url:
                urls.remove(url)
                print(url, '---------------------------------------------------')
                
                # print ('found----------------------------------------------------')


            # for goto in url.css('.listicon.clearfix.margin-btm-60-md.margin-btm-20-sm.margin-top-20-sm.js-content.hide-sm .nolist.flex.flex-wrap .col-xs-12.col-md-3 a::attr(href)').extract():
            #     goto = response.urljoin(goto)
            #     yield scrapy.Request(url=goto, callback=self.get_each_brand_li)

    def get_each_brand_li(self, response):
        for link in response.css('.border-btm-grey-sm.margin-btm-10-sm'):
            if not link:
                continue
            for goto in link.css('.listicon.clearfix.margin-btm-60-md.js-content.margin-btm-20-sm.margin-top-20-sm.hide-sm .nolist.flex.flex-wrap .col-xs-12.col-md-3 a::attr(href)').extract():
                goto = response.urljoin(goto)
                yield scrapy.Request(url=goto, callback=self.get_product_data)

    def get_product_data(self, response):
        pdf_files = response.css('.js-specs-doc.clearfix .doc-link.flex div>a::attr(href)').extract()
        if len(pdf_files) == 0:
            return
        
        # for pdf in pdf_files:
        #     pdf = pdf.replace(' ', '%20') # removing spaces from the pdf link
        #     manual = Manual()
        #     bread_crums = response.css('.breadcrumbs.js-breadcrumbs.hidden-print.w-100 .row .col-xs-12 ul>li')
        #     manual["product"] = bread_crums[-2].css('.js-ellipsis *::text').extract_first()
        #     brand = response.css('.product-detail-title.no-margin-btm a *::text').extract_first()
        #     manual["brand"] = brand.strip()
        #     thumb = response.css('.image-gallery-main-image.js-image-gallery-main-image.js-image-zoom-image.image-gallery-main-image-0::attr(data-large-image)').extract_first()
        #     manual["thumb"] = response.urljoin(thumb)
        #     # nested_fonts = response.css('.product-detail-title.no-margin-btm::text').extract_first()
        #     # model = nested_fonts.css('font ::text').extract_first()
        #     model = response.css('.product-detail-title.no-margin-btm::text').extract_first()
        #     manual["model"] = model
        #     # manual["model"] = model.strip()
        #     manual["source"] = self.name
        #     manual["file_urls"] = [response.urljoin(pdf)]
        #     manual["url"] = response.urljoin('')
        #     manual["type"] = response.css('.js-specs-doc.clearfix .doc-link.flex div>a *::text').extract_first()
        #     print(manual)
        #     yield manual