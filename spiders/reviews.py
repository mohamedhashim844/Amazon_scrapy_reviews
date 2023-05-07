import scrapy
from scrapy.utils.response import open_in_browser

reviews_url = 'https://www.amazon.com/product-reviews/B00DBL0NLQ'
asin_list  =['B00DBL0NLQ']


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    def start_requests(self):
        for asin in asin_list:
            url = reviews_url.format(asin)
            yield scrapy.Request(url)
    def parse(self, response):
        #open_in_browser(response)
        for reviews in response.css('[data-hook="review"]'):
            item = {
                'title':reviews.css('[data-hook="review-title"] span::text').get(),
                'date':reviews.css('[data-hook="review-date"]::text').get(),
                'review':reviews.css('[data-hook="review-body"] span::text').get()
            }
            yield item
    
        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))

