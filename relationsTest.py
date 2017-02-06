#!/usr/bin/python3.5

from sys import argv
from watson_developer_cloud import AlchemyLanguageV1
import json
import os
import pprint

script, link = argv

ALCHEMY_LANGUAGE_KEY = "c251be18000cca3f91ffcdf95b9ae67c5b8f6ef1"
alchemy_language = AlchemyLanguageV1(api_key=ALCHEMY_LANGUAGE_KEY)

def relations(link):
    #response is set to json.dumps (string data type) of the relation found in the article
    response = json.dumps(alchemy_language.relations(url=link, max_items=1), indent=2)
    
    #obj is set to json.loads (object format) of the string that response was set to
    obj = json.loads(response)

    return obj

#sets info to the relation
info = relations(link)

for i in info["relations"]:
    for j in i.items():
        for k in j:
            if (isinstance(k, dict)):
                for l in k.items():
                    for m in l:
                        print(m)
