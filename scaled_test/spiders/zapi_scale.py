import base64

import scrapy


class ZapiScaleSpider(scrapy.Spider):
    name = 'zapi_scale'
    allowed_domains = ['martinhollisfh.com']
    # start_urls = ['https://www.martinhollisfh.com/']

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        'DOWNLOADER_MIDDLEWARES': {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'ZYTE_API_KEY': "APIKEY",
        "ZYTE_API_TRANSPARENT_MODE": True,
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        # 'CLOSESPIDER_PAGECOUNT': 100,
    }

    def __init__(self, referer='https://www.google.com', req=1000, *args, **kwargs):
        super(ZapiScaleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.referer = referer
        self.req = req

    def start_requests(self):
        for url in self.start_urls:
            for i in range(int(self.req)):
                yield scrapy.Request(url=url, meta={
                    "zyte_api": {
                        "browserHtml": True,
                        "actions": [
                            {
                                "action": "waitForTimeout",
                                "timeout": 5,
                                "onError": "return"
                            }
                        ],
                        'requestHeaders': {
                            'referer': self.referer,
                        },
                        "javascript": True,
                    }
                }, callback=self.parse, dont_filter=True)

    def parse(self, response):

        yield {
            'response': response.status,
            'url': response.url,
            # 'browserHtml': response.text,
        }
