#!/usr/bin/python3.5

from sys import argv
from watson_developer_cloud import AlchemyLanguageV1
import json

script, link = argv

ALCHEMY_LANGUAGE_KEY = "c251be18000cca3f91ffcdf95b9ae67c5b8f6ef1"
alchemy_language = AlchemyLanguageV1(api_key=ALCHEMY_LANGUAGE_KEY)

def relations(link):
    #response is set to json.dumps (string data type) of the relation found in the article
    response = json.dumps(alchemy_language.relations(url=link, max_items=2), indent=2)
    
    #obj is set to json.loads (object format) of the string that response was set to
    obj = json.loads(response)

    return obj

"""
    This block of code traverses the dictionary that the relations call returns from Watson.
    This will give a subject, action, and object of an individual claim as well as the claim itself.
    @param subject: the noun of the claim that is performing the action
    @param object: the noun of the claim that is being acted upon
    @param action: the verb of the claim that the subject is using on the object
    
    TODO: Need to find a way to get more than one claim from a single article
    TODO: Potentially less arbitrary commenting
"""
#sets info to the relation
info = relations(link)

subject = ""
isSubPre = 0
isSubject = 0
sentence = ""
isSentence = 0
action = ""
isAction = 0
obj = ""
isObjPre = 0
isObj = 0

for i in info["relations"]:
    for j in i.items():
        #j is the base list of relations (location subject sentence action object)
        for k in j:
            # k is each item in the relations
            # location is a dict
            # subject is a dict
            # sentence is a string
            # action is a dict
            # object is a dict

            if (isSentence == 1):
                sentence = k
                isSentence = 0
            if (k == "subject"):
                isSubPre = 1
            elif (k == "object"):
                isObjPre = 1
            elif (k == "sentence"):
                isSentence = 1

            if (isinstance(k, dict)):
                for l in k.items():
                    # l is the contents of k (excluding the sentence itself which is present in its primitive form in k)
                    # the first is the location or group of people
                    # the second is the subject
                    # the third and fourth are the lemmatized version of the verb and how its present in the article
                    # the fifth is the object the verb acts upon

                    for m in l:
                        # m is the primitive instances of each object extracted in l
                        if (isSubject == 1):
                            subject = m
                            isSubject = 0
                        elif (isObj == 1):
                            obj = m
                            isObj = 0
                        
                        if (isSubPre == 1):
                            isSubject = 1
                            isSubPre = 0
                        elif (isObjPre == 1):
                            isObj = 1
                            isObjPre = 0

                        if (isAction == 1):
                            action = m
                            isAction = 0
                        if (m == "lemmatized"):
                            isAction = 1
print(subject)
print(obj)
print(action)
print(sentence)
