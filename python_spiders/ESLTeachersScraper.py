import scrapy
import requests
import pyperclip
from scrapy import Selector

page = 15
Resumes2 = []

## you can change the range to get this script to scrape as many pages as you want
## it starts from page 17 because I have already scraped pages 1 to 16

for boh in range(1,8):
    resESL = requests.get('http://www.esl-teachersboard.com/cgi-bin/esl/index.pl?page=' + str(page))
    selESL = Selector( text = resESL.text )
    Resumes = selESL.css('dd.thread > a::attr(href)').extract()
    i = 0
    ## Turning relative URLs into absolute URLs
    for resume in Resumes:
        resumeURL = 'http://www.esl-teachersboard.com/' + Resumes[i]
        Resumes2.append(resumeURL)
        i = i + 1

    page = page + 1

teachers = {}

for pageLink in Resumes2:
    resResume = requests.get(pageLink)
    selResume = Selector( text = resResume.text )
    teacherName = selResume.css('span.msg_poster::text').extract()
    teacherEmail = selResume.css('span.msg_email > a::text').extract()
    teacherMessage = selResume.css('div.msg_text p::text').extract()
    
## I have to create a list with TeacherEmail and TeacherMessage first, and then pass it to the dictionary
    teachers[str(teacherName)] = []
    emailAndMessage = [teacherEmail, teacherMessage]
    
## Creating the dictionary, {name: [email, text]}

    teachers[str(teacherName)].extend(emailAndMessage)

## print(len(teachers))

import csv

f = open('ESLTeachersBoard.csv', 'wb')
with open('ESLTeachersBoard.csv', 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    for name, [email, text] in teachers.items():
       writer.writerow([name, email, text])

pyperclip.copy(str(Resumes2))

