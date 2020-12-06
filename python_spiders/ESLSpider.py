import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import pyperclip

ESLjobs = {}

class ESLspider(scrapy.Spider):
    name = "eslspider"

    def start_requests( self ):
        urls = ['http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=13',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=14',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=15',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=16',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=17',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=18',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=19',
                'http://www.esl-teachersboard.com/cgi-bin/intl/index.pl?page=20'
                ]
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse_front )

    def parse_front ( self, response ):
        job_ad = response.css('dd.thread')
        job_ad_link = job_ad.xpath( './a/@href' )
        links_to_follow = job_ad_link.extract()
        
        for url in links_to_follow:
            yield response.follow( url = url, callback = self.parse_pages )

    def parse_pages ( self, response ):

        # Direct to the job title text
        job_title = response.xpath('//div[contains(@class, "msg_headln")]/text()')
        # Extract and clean the job title text. We use extract_first instead of extract because we
        # want a string, not a list
        job_title_ext =  job_title.extract()

        # Direct to the job ad poster
        job_poster = response.xpath('//span[contains(@class, "msg_poster")]/text()')
        # Extract and clean the job poster text
        job_poster_ext =  job_poster.extract()

        # Direct to the job ad email
        job_email = response.xpath('//span[contains(@class, "msg_email")]/a/text()')
        # Extract and clean the job ad email text
        job_email_ext =  job_email.extract()

        # Direct to the job ad date
        job_date = response.xpath('//span[contains(@class, "msg_date")]/text()')
        # Extract and clean the job ad date text
        job_date_ext =  job_date.extract()

        # Direct to the job ad text
        job_text = response.xpath('//div[contains(@class, "msg_text")]//text()')
        # Extract and clean the job ad email text
        job_text_ext =  job_text.extract()
        
        JobTitle = str(job_title_ext)
        JobPoster = str(job_poster_ext)
        JobEmail = str(job_email_ext)
        JobDate = str(job_date_ext)
        JobText = str(job_text_ext)

##        jobData = [JobPoster, JobEmail, JobDate, JobText]
##        ESLjobs[JobTitle].extend(jobData)

#        ESLjobs[JobTitle] = [JobPoster, JobEmail, JobDate, JobText]

        f = open('ESLTeachersBoard.csv', 'ab')
        with open('ESLTeachersBoard.csv', 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([JobTitle, JobPoster, JobEmail, JobDate, JobText])



    # for job_title_ext, [job_poster_ext, job_email_ext, job_date_ext, job_text_ext] in ESLjobs.items():
##
##
##
##        
##
##esl_dict = dict()
##
##        
##msg_poster
##msg_email
##msg_date

process = CrawlerProcess()
process.crawl(ESLspider)
process.start()
