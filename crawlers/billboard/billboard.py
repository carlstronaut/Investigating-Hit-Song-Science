import scrapy

class BillboardSpider(scrapy.Spider):
    name = 'billboard'
    start_urls = {'https://www.billboard.com/charts/dance-club-play-songs/1976-08-28'}

    calls = 0

    def parse(self, response):
        # Find date information
        DATE_SELECTOR = './/button[@id = "dateSearchSubmit"]/@data-%s'
        year = response.xpath(DATE_SELECTOR % 'year').get()
        month = response.xpath(DATE_SELECTOR % 'month').get()
        day = response.xpath(DATE_SELECTOR % 'day').get()

        # Find all tracks
        TRACK_SELECTOR = './/table/tbody/tr[td[@class = "item-details"]]'
        for row in response.xpath(TRACK_SELECTOR):

            POSITION_SELECTOR = './td[3]/text()'
            TITLE_SELECTOR = './/td[@class = "item-details"]/div[@class = "item-details__title"]/text()'
            ARTIST_SELECTOR = './/td[@class = "item-details"]/div[@class = "item-details__artist"]/text()'

            yield {
            'position': row.xpath(POSITION_SELECTOR).get(),
            'title':    row.xpath(TITLE_SELECTOR).get(),
            'artist':   row.xpath(ARTIST_SELECTOR).get(),
            'year':     year,
            'month':    month,
            'day':      day,
            }

        # self.calls += 1

        # Redirect to next week's chart
        if self.calls < 2:
            NEXT_PAGE_SELECTOR = './/ul[@class = "dropdown__date-selector-inner"]/li[2]/a/@href'
            next_page = response.xpath(NEXT_PAGE_SELECTOR).get()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
