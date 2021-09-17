# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Manual(scrapy.Item):
    model = scrapy.Field() # product name without brand
    model_2 = scrapy.Field() # alternative product name (optional)
    brand = scrapy.Field() # brand name
    product = scrapy.Field() # product (for example "washing machines")
    file_urls = scrapy.Field() # url to PDF
    eans = scrapy.Field() # optional product EANs
    files = scrapy.Field() # internal
    type = scrapy.Field() # type, for example "quick start guide", "datasheet" or "manual" (optional if type = manual)
    url = scrapy.Field() # url of the page containing link to pdf
    thumb = scrapy.Field() # thumbnail (optional)
    source = scrapy.Field() # hostname without http/www to identify the source, for example dyson.com or walmart.com
