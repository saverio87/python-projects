import csv
import scrapy
from scrapy.crawler import CrawlerProcess

class AirBnBspider(scrapy.Spider):
    name = "airbnbspider"

    def start_requests( self ):
        urls = [];
#
#        urls = ['https://www.airbnb.com/s/Foligno--Province-of-Perugia--Italy/homes?tab_id=all_tab&refinement_paths%5B%5D=%2Fhomes&query=Foligno%2C%20Province%20of%20Perugia&place_id=ChIJK5bow9uFLhMRL6spSC7QwHA&checkin=2020-07-14&checkout=2020-07-15&adults=2&source=structured_search_input_header&search_type=search_query']
        last_page = 80 ## so that it includes 280
        for i in range(0,last_page,20):
            page = ('https://www.airbnb.com/s/Foligno--Province-of-Perugia--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJK5bow9uFLhMRL6spSC7QwHA&source=structured_search_input_header&search_type=pagination&federated_search_session_id=96b7dd39-d132-4331-8805-6091395e424c&query=Foligno%2C%20Italy&checkin=2020-07-14&checkout=2020-07-15&adults=2&section_offset=4&items_offset={}').format(i);
            urls.append(page);
        
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse_front)

    def parse_front ( self, response ):

        listing = response.css('div._dx669kc')
        listing_url = listing.xpath( './a/@href' )

        links_to_follow = listing_url.extract()
        
        for url in links_to_follow:
            yield response.follow( url = url, callback = self.parse_pages)

    def parse_pages ( self, response ):

        title = response.xpath('//*[@id="site-content"]/div/div/div[1]/div/div/div/section/div[1]/div[1]/h1/text()').extract();
        description = response.xpath('//*[@id="site-content"]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[1]/text()').extract();
        full_desc = response.xpath('//*[@id="site-content"]/div/div/div[4]/div/div/div[1]/div[3]/div/div/div/section/div/div[1]/span/div[2]/div/span//text()').extract();
        avg_score = response.xpath('//span[contains(@class, "_1jpdmc0")]//text()').extract();
        num_reviews = response.xpath('//span[contains(@class, "_1sqnphj")]//text()').extract(); 
        price_night = response.xpath('//span[contains(@class, "_pgfqnw")]//text()').extract();
        service_fee = response.xpath('//span[contains(@class, "_ra05uc")]//text()').extract();
        rooms = response.xpath('//*[@id="site-content"]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[2]//span/text()').extract();
        amenities = response.xpath('//*[@id="site-content"]/div/div/div[4]/div/div/div[1]/div[5]/div/div/div/section/div/section/div[2]//text()').extract();
        hosted_by = response.xpath('//*[@id="site-content"]/div/div/div[7]/div/div/div/section/div/div[1]/div[2]/h2/text()').extract();
        host_languages = response.xpath('//*[@id="site-content"]/div/div/div[7]/div/div/div/section/div/div[2]/div[2]/ul/li[1]//text()').extract();
        host_reviews = response.xpath('//*[@id="site-content"]/div/div/div[7]/div/div/div/section/div/div[2]/div[1]/div[1]/ul/li[1]/div/span[2]//text()').extract();
        host_response_rate = response.xpath('//*[@id="site-content"]/div/div/div[7]/div/div/div/section/div/div[2]/div[2]/ul/li[2]//text()').extract();
        host_response_time = response.xpath('//*[@id="site-content"]/div/div/div[7]/div/div/div/section/div/div[2]/div[2]/ul/li[3]//text()').extract();



        f = open('AirBnbFoligno.csv', 'ab')
        with open('AirBnbFoligno.csv', 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([title,description,full_desc,avg_score,num_reviews,price_night,service_fee,rooms,amenities,hosted_by,host_languages,host_reviews,host_response_rate,host_response_time])



process = CrawlerProcess()
process.crawl(AirBnBspider)
process.start()
