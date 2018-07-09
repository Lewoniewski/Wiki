import urllib.request
import json


def getpage(title):
    url = 'https://pl.wikipedia.org/w/api.php'
    values = {'action': 'query',
              'prop': 'revisions',
              'titles': title,
              'prop': 'revisions',
              'rvprop': 'content',
              'format': 'json',
              'formatversion': 2, }

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    bytes = response.read()
    strings = bytes.decode('utf-8')
    dictionary = json.loads(strings)
    content = dictionary['query']['pages'][0]['revisions'][0]['content']
    return content

def saveToFile(plik, strona):
    text_file = open(plik, "w", encoding='utf-8')
    text_file.write(strona)
    text_file.close()

def loadArticleNames(plik):
    text_file = open(plik, "r")
    list = text_file.read().splitlines()
    text_file.close()
    return list

namesOfArticles = loadArticleNames('pliki.txt')
n=0
for i in namesOfArticles:
    saveToFile('zapisane'+str(n)+'.txt', getpage(i))
    n=n+1

print(getpage('Poznań'))
