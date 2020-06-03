import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
import csv

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata

soup= make_soup("file:///Users/zhouxiao/Desktop/0000320193-20-000052-xbrl/a10-qq220203282020.htm#s1D43D3A139195BB08634F3B6B1743277")

# unknowdatasaved = ""
# for record in soup.findAll('tr'):
#     unknowdata = ""
#     for data in record.findAll('td'):
#         unknowdata=unknowdata+","+data.text
#     unknowdatasaved=unknowdatasaved + "\n" + unknowdata[1:]
#
# file = open(os.path.expanduser("/Users/zhouxiao/Desktop/Python/summer project/balance_sheet.xlsx"),"wb")
# file.write(bytes(unknowdatasaved,encoding="ascii",errors='ignore'))

rows = soup.find('div', attrs={'style':'line-height:120%;text-align:justify;padding-left:0px;text-indent:0px;font-size:10pt;'}).find_all('tr')

file = open('income.csv','w')
writer = csv.writer(file)

#
for row in rows:
    itermnames = row.find_all('div', attrs={'style': 'text-align:left;font-size:9pt;'})
    numbers = row.find_all('div', attrs={'style': 'text-align:right;font-size:9pt;'})
    itermname=""
    for i in itermnames:
        itermname = i.text.strip()
    march2019_6=''
    march2019=''
    march2020_6=''
    march2020=''
    for i in range(len(numbers)):
        march2020 = numbers[0].text.strip()
        march2019 = numbers[1].text.strip()
        march2020_6 = numbers[2].text.strip()
        march2019_6 = numbers[3].text.strip()

    print(itermname + ' ' + march2020 + ' ' + march2019 + ' ' + march2020_6 + ' ' + march2019_6)
    writer.writerow([itermname.encode('utf-8'), march2020.encode('utf-8'), march2019.encode('utf-8'),march2020_6.encode('utf-8'),march2019_6.encode('utf-8')])
#

# file.close()
# #


