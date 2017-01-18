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
    response = json.dumps(alchemy_language.keywords(url=link), indent=2)
    info = json.loads(response)
    return info

print(keywords(link))
