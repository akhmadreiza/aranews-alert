import requests
from bs4 import BeautifulSoup
import hashlib
import time
from datetime import date

strHashed = None

def executeUrl(targetUrl):
    attempt = 1
    while True:
        print('begin accessing url', targetUrl, 'for attempt', attempt)
        try:
            page = requests.get(targetUrl, timeout=(10,10))
            print('done accessing url', targetUrl, 'after', attempt, 'attempt')
            break
        except:
            attempt = attempt + 1
            if attempt <= 50:
                print('timeout accessing url', targetUrl, 'trying again..')
            else:
                break 
    return page

def hashInput(strInput):
    hash_object = hashlib.md5(strInput.encode())
    return hash_object.hexdigest()

def keywordMatched(newsUrl, newsTitle):
    result = False
    keyWordTitleFoundList = []
    keyWordParagraphFoundList = []

    #MNC Group, MNC Hary Tanoe, Hary Tanoesoedibjo, Tanoesoedibjo, MNC Land, MNC Vision, MNC Asset Management, MNC Bank, MNCN, Media Nusantara Citra, Global Mediacom
    searchKeyWordPerindo=['MNC Group', 'MNC Hary Tanoe', 'Hary Tanoesoedibjo', 'Tanoesoedibjo', 'MNC Land', 'MNC Vision', 'MNC Asset Management', 'MNC Bank', 'MNCN', 'Media Nusantara Citra', 'Global Mediacom']
    
    #search title first
    for keyword in searchKeyWordPerindo:
        if keyword.casefold() in newsTitle.casefold():
            keyWordTitleFoundList.append(keyword)
            result = True
    
    if result:
        outputFile = open('alert-result.txt', 'a+')
        print('found keywords:', keyWordTitleFoundList, file=outputFile)
        outputFile.close

    if not result:
        #search within url
        #use this for test https://www.wartaekonomi.co.id/read287070/top-3-saham-paling-diborong-vs-saham-paling-diobral-usai-lebaran
        targetUrl = newsUrl
        page = executeUrl(targetUrl)
        soup = BeautifulSoup(page.text, 'html.parser')
        paragraphList = soup.find_all('p', {'style':'text-align: justify;'})

        for keyword in searchKeyWordPerindo:
            for paragraph in paragraphList:
                paragraphText = paragraph.text
                if keyword.casefold() in paragraphText.casefold():
                    keyWordParagraphFoundList.append(keyword)
                    result = True
    
    if result:
        outputFile = open('alert-result.txt', 'a+')
        print('found keywords:', keyWordParagraphFoundList, file=outputFile)
        outputFile.close
    else:
        print('keyword not found both in title and paragraph')

    return result

def initAlerter():
    global strHashed

    while True:
        if strHashed is None:
            print('init...')
        else:
            print('sleep for 30 seconds...')
            time.sleep(30)
        
        strToday = str(date.today()).replace('-','')
        targetUrl = 'https://www.wartaekonomi.co.id/indeks/'+strToday+'/1'
        print('begin search url', targetUrl)
        page = executeUrl(targetUrl)
        soup = BeautifulSoup(page.text, 'html.parser')

        indexContainer = soup.find('div', class_='col-xs-9 padding-7px match-height')
        newsList = indexContainer.find_all('p', class_='news-title font-family-alt font-weight-700 no-letter-spacing text-medium')

        news = newsList[0]
        elementUrl = news.find('a')
        newsUrl = elementUrl.get('href')
        newsTitle = elementUrl.text

        tempStrHashed = hashInput(newsUrl+newsTitle)

        if strHashed == tempStrHashed:
            print('no latest news. do nothing....')
        else:
            print('found latest news. proceed....')
            strHashed = tempStrHashed
            if keywordMatched(newsUrl, newsTitle):
                outputFile = open('alert-result.txt', 'a+')
                print(newsUrl, newsTitle, sep='|', file=outputFile)
                outputFile.close
        print('end search\n\n')

initAlerter()