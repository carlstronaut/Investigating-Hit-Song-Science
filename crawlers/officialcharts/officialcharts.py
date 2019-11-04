import scrapy

class OfficialChartsSpider(scrapy.Spider):
    name = 'officialcharts'
    start_urls = {'https://www.officialcharts.com/charts/dance-singles-chart/19940703/104/'}
    calls = 0

    MONTH_DICT = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
    }

    def parse(self, response):
        # Find date information
        DATE_SELECTOR = './/select[@class = "%s-search"]/option[@selected = "selected"]/text()'
        year = response.xpath(DATE_SELECTOR % 'year').get()
        month = response.xpath(DATE_SELECTOR % 'month').get()
        day = response.xpath(DATE_SELECTOR % 'day').get()

        # Find all tracks
        TRACK_SELECTOR = './/table[@class = "chart-positions"]/tr[td/span[@class = "position"]]'
        for row in response.xpath(TRACK_SELECTOR):
            POSITION_SELECTOR = './/td/span[@class = "position"]/text()'
            TITLE_SELECTOR = './/div[@class = "title-artist"]/div[@class = "title"]/a/text()'
            ARTIST_SELECTOR = './/div[@class = "title-artist"]/div[@class = "artist"]/a/text()'

            yield {
            'position': row.xpath(POSITION_SELECTOR).get(),
            'title':    row.xpath(TITLE_SELECTOR).get(),
            'artist':   row.xpath(ARTIST_SELECTOR).get(),
            'year':     year,
            'month':    self.MONTH_DICT[month],
            'day':      day,
            }

        # self.calls += 1
        # Redirect to next week's chart
        if self.calls < 2:
            NEXT_PAGE_SELECTOR = 'a.next ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).get()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
