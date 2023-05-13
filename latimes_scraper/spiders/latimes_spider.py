from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LATimesCrawlSpider(CrawlSpider):
    name = 'latimes_crawlspider'
    allowed_domains = ['latimes.com']
    start_urls = ['https://www.latimes.com/sitemap/2022'] 

    # Use Rules to specify how the CrawlSpider should follow links
    rules = [
        Rule(LinkExtractor(restrict_css='a'), callback='parse_article', follow=True),
        Rule(LinkExtractor(restrict_css='a.next'), follow=True)
    ]

    # You can use the following function to customize your search by specifying certain words
    def contains_keywords(self, text, keywords):
        return any(keyword.lower() in text.lower() for keyword in keywords)

    def parse_article(self, response):
        # Replace the following list with the keywords you want to filter articles by
        keywords = ['covid']

        title = response.css('h1::text').get()
        content = ' '.join(response.css('p::text').getall())

        if '/story/2022-' in response.url:
            if self.contains_keywords(title, keywords) or self.contains_keywords(content, keywords):
                yield {
                    'url': response.url,
                    'title': title,
                    # 'content': content,
                }

