import requests
from bs4 import BeautifulSoup

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

#MNC Group, MNC Hary Tanoe, Hary Tanoesoedibjo, Tanoesoedibjo, MNC Land, MNC Vision, MNC Asset Management, MNC Bank, MNCN, Media Nusantara Citra, Global Mediacom
searchKeyWordPerindo=['MNC Group', 'MNC Hary Tanoe', 'Hary Tanoesoedibjo', 'Tanoesoedibjo', 'MNC Land', 'MNC Vision', 'MNC Asset Management', 'MNC Bank', 'MNCN', 'Media Nusantara Citra', 'Global Mediacom']

#search title first
# for keyword in searchKeyWordPerindo:
#     if keyWord.casefold() in newsTitle.casefold():
#         return True

#search within url
#use this for test https://www.wartaekonomi.co.id/read287070/top-3-saham-paling-diborong-vs-saham-paling-diobral-usai-lebaran
targetUrl = 'https://www.wartaekonomi.co.id/read287070/top-3-saham-paling-diborong-vs-saham-paling-diobral-usai-lebaran'
page = executeUrl(targetUrl)
soup = BeautifulSoup(page.text, 'html.parser')
paragraphList = soup.find_all('p', {'style':'text-align: justify;'})

keyWordParagraphFoundList = []
result = False

for keyword in searchKeyWordPerindo:
    tempKeyword = keyword
    for paragraph in paragraphList:
        paragraphText = paragraph.text
        if keyword.casefold() in paragraphText.casefold():
            keyWordParagraphFoundList.append(keyword)
            result = True
            break

if result:
    outputFile = open('alert-result.txt', 'a+')
    print('found keywords:', keyWordParagraphFoundList, file=outputFile)
    outputFile.close