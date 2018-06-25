#!/usr/bin/python
# -*- coding: utf-8 -*-
import gzip, re, os, inspect

langs=["be","de","en","fr","pl","ru","uk"]

for lang in langs:
    print lang
    with open("infoboxes/"+lang+".txt","r") as gg:
        infoboksy=gg.read().splitlines()
    
    artykul=0
    tytul=""
    ns=0
    tekst=0
    sl={}

    zl={}
    lista=set()
    with gzip.open("dumps/"+lang+"_templates.csv.gz","r") as gg:
        for line in gg:
            part=line.replace("\n","").split("\t\t")
            if part[0] in infoboksy:
                stati=part[1].split("|||")
                for tt in stati[:-1]:
                    lista.add(tt.replace('\\"','"'))

    f = open(lang+".txt", "w")
    for xxx in lista:
        f.write(xxx+"\n")
    f.close()
