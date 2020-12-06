import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import pyperclip


class ESLspider(scrapy.Spider):
    name = "eslspider"

    def start_requests( self ):

        urls = []
        pages_to_scrape=41
        for i in range(20,pages_to_scrape):
            page = ('http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page={}').format(i);
            urls.append(page);
        
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse_front )

    def parse_front ( self, response ):
        jobAd = response.css('dd.thread')
        jobAdLink = jobAd.xpath( './a/@href' )

        links_to_follow = jobAdLink.extract()
        
        for url in links_to_follow:
            yield response.follow( url = url, callback = self.parse_pages )

    def parse_pages ( self, response ):

        job_title = response.xpath('//*[@id="msg_wrap"]/div[1]/text()')
        job_poster = response.xpath('//*[@id="msg_wrap"]/div[2]/span[1]/text()')
        job_email = response.xpath('//*[@id="msg_wrap"]/div[2]/span[2]/a/text()')
        job_date = response.xpath('//*[@id="msg_wrap"]/div[2]/span[3]/text()')
        job_content = response.xpath('//*[@id="msg_wrap"]/div[3]//text()')

        Title = job_title.extract_first()
        Poster = job_poster.extract_first()
        Email = job_email.extract_first()
        Date = job_date.extract_first()
        Content = ' '.join(job_content.extract())

        

        f = open('ESLJobAds.csv', 'ab')
        with open('ESLJobAds.csv', 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([Title, Poster, Email, Date, Content])



process = CrawlerProcess()
process.crawl(ESLspider)
process.start()
