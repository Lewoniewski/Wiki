from __future__ import division
import urllib, json, sys, os, time, re

startlangs = []
startnames = []
startlevels = []

nss = 1

f = open('startlist.txt', "r").readlines()
for line in f:
    if "\t" in line:
        line = line.replace("https://", "")
        line = line.replace(".wikipedia.org/wiki/", "\t")
        (startlevel, startlang, startname) = line.split("\t")
    else:
        line = line.replace("https://", "")
        line = line.replace("\n", "")
        (startlang, startname) = line.split(".wikipedia.org/wiki/")
        startlevel = 0
    print line

    startlangs.append(startlang)
    startnames.append(startname)
    startlevel = int(startlevel)
    startlevels.append(startlevel)

levels = 0 # 0 - бесконечно, пока есть вложенные категории
level = 1
daleecats = []
daleearts = []
allarticles = []

def listgenerator(lang, names, level=1, z=0):
    
    artlist = []
    catlist = []
    for x in range(0, len(names)):
        prodolzajem=0
        name = names[x]
        if level>1:
            name = name.encode('utf-8')
        print "## " + lang + " " + str(level) + " (" + str(round(((x+1)/(len(names))*100),1)) + "%) ## " + name.decode('utf-8')
        url = urllib.unquote("https://"+lang+".wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=" + name + "&format=json&eilimit=500&rawcontinue")
        try:
            response = urllib.urlopen(url)
        except IOError:
            print "Try again in 50 second"
            time.sleep(50)
            response = urllib.urlopen(url)
        m2 = response.read()
        try:
            data = json.loads(m2)
            normalno=1
        except:
            if nss == 0:
                szb = re.findall(r'"ns":0,"title":"([^"]+)"}', str(m2))
            if nss == 1:
                szb = re.findall(r'"ns":1,"title":"([^"]+)"}', str(m2))
            for x in szb:
                artlist.append(x)
            szb = re.findall(r'"ns":14,"title":"([^"]+)"}', str(m2))
            if len(szb)>0:
                for x in szb:
                    catlist.append(x)
                    
            nname1 = re.findall(r'"eicontinue":"([^"]+)"}', str(m2))
            nname=nname1[0]
            normalno=0

        if normalno==1:
            elcount = len(data['query']['embeddedin'])

            for y in range(0, elcount):
                if data['query']['embeddedin'][y]['ns'] == nss :
                    artlist.append(data['query']['embeddedin'][y]['title'])
                if data['query']['embeddedin'][y]['ns'] == 14 :
                    catlist.append(data['query']['embeddedin'][y]['title'])

            if "query-continue" in data:
                 nname=data['query-continue']['embeddedin']['eicontinue']
                 prodolzajem=1
                    
        if normalno==0:
                for x in szb:
                    artlist.append(x)
                if len(nname)>1:
                    prodolzajem=1

        if prodolzajem==1:
            while prodolzajem==1:
                prodolzajem=0
                print nname.encode('utf-8')
                url2 = url + "&eicontinue=" + urllib.unquote(nname).encode('utf-8')
                try:
                    response = urllib.urlopen(url2)
                except IOError:
                    print "Try again in 50 second"
                    time.sleep(50)
                    response = urllib.urlopen(url2)
                m2 = response.read()
                try:
                    data = json.loads(m2)
                except:
                    #with open('error.txt', 'w') as f:
                    #    dobavlajem = f.write(m2)
                    if nss == 0:
                        szb = re.findall(r'"ns":0,"title":"([^"]+)"}', str(m2))
                    if nss == 1:
                        szb = re.findall(r'"ns":1,"title":"([^"]+)"}', str(m2))
                    for x in szb:
                        artlist.append(x)
                    szb = re.findall(r'"ns":14,"title":"([^"]+)"}', str(m2))
                    if len(szb)>0:
                        for x in szb:
                            catlist.append(x)                    
                    nname1 = re.findall(r'"eicontinue":"([^"]+)"}', str(m2))
                    nname=nname1[0]
                    if len(nname)>1:
                        prodolzajem=1
                    continue
                    
                elcount = len(data['query']['embeddedin'])
                for y in range(0, elcount):
                    if data['query']['embeddedin'][y]['ns'] == nss :
                        artlist.append(data['query']['embeddedin'][y]['title'])
                    if data['query']['embeddedin'][y]['ns'] == 14 :
                        catlist.append(data['query']['embeddedin'][y]['title'])
                        
                if "query-continue" in data:
                    nname = data['query-continue']['embeddedin']['eicontinue']
                    prodolzajem=1

    zdublart = len(artlist)
    zdublcat = len(catlist)
    artlist = list(set(artlist))
    catlist = list(set(catlist))
    print "--------------"
    print "$$$$ " + lang + " " + str(level) + " level ### New Articles: " + str(len(artlist)) + " (with dublicates: " + str(zdublart) + ")"
    print "$$$$ " + lang + " " + str(level) + " level ### New Categories: " + str(len(catlist)) + " (with dublicates: " + str(zdublcat) + ")"
    print "--------------"

    if not os.path.exists(lang+str(z)+"/articles"):
        os.makedirs(lang+str(z)+"/articles")
    f = open(lang+str(z)+'/articles/'+str(level)+'.txt', 'w')
    for item in artlist:
      f.write("%s\n" % item.encode('utf-8'))
    f.close()

    if not os.path.exists(lang+str(z)+"/categories"):
        os.makedirs(lang+str(z)+"/categories")
    f = open(lang+str(z)+'/categories/'+str(level)+'.txt', 'w')
    for item in catlist:
      f.write("%s\n" % item.encode('utf-8'))
    f.close()

    global daleecats
    daleecats = catlist

    global daleearts
    daleearts = artlist

for z in range (0, len(startnames)):
    startnamess = []
    startnamess.append(startnames[z])

    listgenerator(startlangs[z], startnamess, 1, z)
    allarticles.extend(daleearts)
    level = 1
    if startlevels[z] == 0:
        while len(daleecats) > 0:
            level = level + 1
            listgenerator(startlangs[z], daleecats, level)
            allarticles.extend(daleearts)
    else:
        for x in range (2,startlevels[z]+1):
            listgenerator(startlangs[z], daleecats, x)
            allarticles.extend(daleearts)

    zdublall = len(allarticles)
    allarticles = list(set(allarticles))

    print "############# " + startlangs[z] + " #########"
    print "All articles: " + str(len(allarticles)) + " (with dublicates: " + str(zdublall) + ")"
    print "##########################"

    f = open(startlangs[z] + str(z) + '/allarticles.txt', 'w')
    for item in allarticles:
        f.write("%s\n" % item.encode('utf-8'))
    f.close()

    allarticles = []
    daleecats = []
    daleearts = []
