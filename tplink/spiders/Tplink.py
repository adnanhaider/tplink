import logging
import scrapy
import os
from scrapy import Spider
from tplink.items import Manual


logger = logging.getLogger(__name__)

class Tplink(Spider):
    name = "tplink"
    start_urls = [
        "https://www.tp-link.com/en/support/download/"
        ]
    
    def parse(self, response):
        urls = response.css('#list .item .item-box a::attr(href)').getall()
        p_names = response.css('.tp-m-hide::text').getall()
        product_names = ''
        product_name_model_dictionary = {}
        product_container = response.css('.item-box')
        for index, p_name in enumerate(p_names):
            if p_name.count('>') > 1:
                product_names = (p_name.split('>')[-2].strip() + " " + p_name.split('>')[-1].strip())

            models = product_container[index].css('.ga-click::text').getall()
            # print(product_names,' ========== ' ,models, ' models=============================')
            # return
            temp_dic = {product_names: models}
            product_name_model_dictionary.update(temp_dic)
        
        # print(product_name_model_dictionary)    
        # return

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


            yield scrapy.Request(url=url, callback=self.get_pdf, meta={"dict":product_name_model_dictionary})

    def get_pdf(self, response):
        dictionary = response.meta.get('dict')
        manual = Manual()
        versions = response.css('.select-version a::attr(href)').getall()
        # print(response.css('.download-list .ga-click::attr(href)').getall())
        # return
        # print(response.css('.product-name a strong::text').get(),'========')
        # return
        if len(versions):
            # get pdf for all the versions
            for version in versions:
                # self.get_version_pdf(version)
                pass
        else:
            c_url = response.request.url
            lang = c_url.split('/')[4]
            pdfs = response.css('.download-list .ga-click::attr(href)').getall()
            model = response.css('#model-title-name::text').get()
            thumb = response.css('.product-name img::attr(src)').get()
            product = ''
            # print(model, '-----------------------model-----')
            for key,value in dictionary.items():
                if model in value:
                    # print('____found-----------', model)
                    product = key
            # return
            manual["product"] = product
            manual["brand"] = 'Tp-link'
            manual["thumb"] = thumb
            manual["model"] = model
            manual["source"] = 'tp-link.com'
            manual["file_urls"] = pdfs
            manual["url"] = c_url
            manual["type"] = 'Manual'
            manual["product_lang"] =  lang 
            print(manual,'-----------------------------------------------------------')

            
            
            
        # for link in versions:
        #     if not link:
        #         continue
        #     for goto in link.css('.listicon.clearfix.margin-btm-60-md.js-content.margin-btm-20-sm.margin-top-20-sm.hide-sm .nolist.flex.flex-wrap .col-xs-12.col-md-3 a::attr(href)').extract():
        #         goto = response.urljoin(goto)
        #         yield scrapy.Request(url=goto, callback=self.get_product_data)

    # def get_product_data(self, response):
    #     pdf_files = response.css('.js-specs-doc.clearfix .doc-link.flex div>a::attr(href)').extract()
    #     if len(pdf_files) == 0:
    #         return
        
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