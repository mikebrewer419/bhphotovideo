import scrapy
import cfscrape

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['bhphotovideo.com']
    start_urls = ['https://bhphotovideo.com']
    # user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"

    # def start_requests(self):
    #     for url in self.start_urls:
    #         token, agent = cfscrape.get_tokens(url, self.user_agent)
    #         yield scrapy.Request(url=url, cookies=token, headers={'User-Agent': agent})

    def parse(self, response):
        yield from response.follow_all(css='header div nav div ul li a', callback=self.parse_category)
    
    def parse_category(self, response):
        yield from response.follow_all(css='a[data-selenium=categoryGroupLink]', callback=self.parse_category)
        yield from response.follow_all(css='a[data-selenium=categoryGroupSubcategoriesListItemLink]', callback=self.parse_category)
        links = response.css('[data-selenium=miniProductPageProductImgLink]')[0:10]
        yield from response.follow_all(links, callback=self.parse_product)
       
    def parse_product(self, response):
        yield {
            'categories':  ' / '.join(response.css('[data-selenium="linkCrumb"]::text').getall()[1:-1]),
            'name': response.css('[data-selenium="productTitle"]::text').get(),
            'price': response.css('[data-selenium="pricingPrice"]::text').get(),
            'image_url': response.css('[data-selenium="inlineMediaMainImage"]::attr(src)').get(),
            'bh_id':  response.css('[data-selenium="codeCrumb"]::text').get().split(' ')[1],
            'manufacture_number':  response.css('[data-selenium="codeCrumb"]::text').get().split(' ')[3],
            'reviews': response.css('[data-selenium="reviewsNumber"]::text').get(),
            'key_features': ' / '.join(response.css('[data-selenium="sellingPointsListItem"]::text').getall())
        }
