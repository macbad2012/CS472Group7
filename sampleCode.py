from sys import argv
from watson_developer_cloud import AlchemyLanguageV1
import json
import os

scipt, link = argv

WATSON_KEY = "c251be18000cca3f91ffcdf95b9ae67c5b8f6ef1"
alchemy_language = AlchemyLanguageV1(api_key=WATSON_KEY)

def title(link):
    response = json.dumps(alchemy_language.title(url=link), indent=2)
    info = json.loads(response)
    return info["title"]

def keywords(link):
    response = json.dumps(alchemy_language.keywords(url=link),indent=2)
    info = json.loads(response)
    return info

def authors(link):
    response = json.dumps(alchemy_language.authors(url=link),indent=2)
    info= json.loads(response)
    return info["authors"]

def concepts(link):
    response = json.dumps(alchemy_language.concepts(url=link),indent=2)
    info = json.loads(response)
    return info

def date(link):
    response = json.dumps(alchemy_language.publication_date(url=link),indent=2)
    info = json.loads(response)
    return info

def emotion(link):
    response = json.dumps(alchemy_language.emotion(url=link),indent=2)
    info = json.loads(response)
    return info

def relations(link):
    response = json.dumps(alchemy_language.relations(url=link, max_items=1), indent=2)
    info = json.loads(response)
    return info


for i in keywords(link)["keywords"]:
    if (float(i['relevance']) > 0.5) :
        print i    

print ' '
for i in concepts(link)["concepts"]:
    if (float(i['relevance']) > 0.75) :
        print i        

for i in date(link)["publicationDate"]:
    print i    

"""
info = relations(link)
rel = info["relations"]
print rel['action']
"""
"""print relations(link)"""
