import urllib.request
import json

def getpage(title):
    url = 'https://pl.wikipedia.org/w/api.php'
    values = {
            "action": "query",
            "format": "json",
            "list": "embeddedin",
            "formatversion": "2",
            "eititle": title,
            "eilimit": "500"
            }

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    bytes = response.read()
    strings = bytes.decode('utf-8')
    dictionary = json.loads(strings)
    content = dictionary['query']['embeddedin']
    return dictionary

def getNextPage(title, continuation):
    url = 'https://pl.wikipedia.org/w/api.php'
    values = {
            "action": "query",
            "format": "json",
            "list": "embeddedin",
            "formatversion": "2",
            "eititle": title,
            "eicontinue":continuation,
            "eilimit": "500"
            }

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    bytes = response.read()
    strings = bytes.decode('utf-8')
    dictionary = json.loads(strings)
    return dictionary


def saveListToFile(file, nameOfArticle):
    text_file = open(file, "a", encoding='utf-8')
    text_file.write(nameOfArticle+'\n')
    text_file.close()


def loopGetPages(title):
    currentPage = getpage(title)
    listOfPages = []
    boolean = True
    while boolean == True:
        if('continue' in currentPage):
            if('eicontinue' in currentPage['continue']):
                listOfPages.append(currentPage['query']['embeddedin'])
                formerCurrentPage = currentPage
                currentPage = getNextPage(title,formerCurrentPage['continue']['eicontinue'])
            else:
                boolean = False
        else:
            boolean = False
    listOfPages.append(currentPage['query']['embeddedin'])
    return listOfPages


for i in loopGetPages("Szablon:POL_miasto_infobox"):
    for j in i:
        if (j['ns']==0):
            saveListToFile('names of articles file.txt',j['title'])