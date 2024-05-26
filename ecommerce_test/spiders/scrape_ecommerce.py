import scrapy


class ScrapeEcommerceSpider(scrapy.Spider):
    name = "scrape_ecommerce"
    allowed_domains = ["webscraper.io"]
    base_url = 'https://webscraper.io/test-sites/e-commerce/static/computers/tablets?page='
    start_urls = [base_url + '1']

    def parse(self, response):
        # Determine the total number of pages
        pagination = response.css('ul.pagination')
        pages = pagination.css('a.page-link::text').getall()
        total_pages = int(pages[-2])

        # Iterate through each page
        for page in range(1, total_pages + 1):
            url = self.base_url + str(page)
            yield scrapy.Request(url, callback=self.parse_page)


    def parse_page(self, response):

        product_list=response.xpath("//div[@class='col-md-4 col-xl-4 col-lg-4']")


        for product in product_list:
            product_name = product.css(".title::text").get()
            product_price = product.css("h4.price::text").get()
            product_desc = product.css("p.description::text").get()
            product_review = product.css("p.review-count::text").get()

            yield {"Name": product_name,
                    "Price": product_price,
                    "Desc" : product_desc,
                    "Review count" : product_review

                }
