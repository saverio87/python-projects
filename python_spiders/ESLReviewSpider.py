import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import pyperclip

ESLjobs = {}

class ESLspider(scrapy.Spider):
    name = "eslspider"

    def start_requests( self ):
        urls = ['http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=5',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=6',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=7',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=8',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=9',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=10',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=11',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=12',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=13',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=14',
                'http://www.esl-teachersboard.com/cgi-bin/review/index.pl?page=15'
                ]
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse_front )

    def parse_front ( self, response ):
        reviewThread = response.css('dd.thread')
        reviewThreadLink = reviewThread.xpath( './a/@href' )

        reviewResp = response.css('dd.resp')
        reviewRespLink = reviewResp.xpath( './a/@href' )

        links_to_follow = reviewThreadLink.extract() + reviewRespLink.extract()
        
        for url in links_to_follow:
            yield response.follow( url = url, callback = self.parse_pages )

    def parse_pages ( self, response ):


        review_name = response.xpath('/html/body/div/div[2]/div[3]/div/div[4]/div[1]/text()[1]')
        review_name_ext =  str(review_name.extract())

        review_email = response.xpath('//span[contains(@class, "msg_email")]/a/text()')
        review_email_ext =  review_email.extract_first()

        

        f = open('teachersReviewsEmails.csv', 'ab')
        with open('teachersReviewsEmails.csv', 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([review_name_ext, review_email_ext])



process = CrawlerProcess()
process.crawl(ESLspider)
process.start()
