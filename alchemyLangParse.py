#!/usr/bin/python3.5

from sys import argv
from watson_developer_cloud import AlchemyLanguageV1
import json

script, link = argv

ALCHEMY_LANGUAGE_KEY = "c251be18000cca3f91ffcdf95b9ae67c5b8f6ef1"
alchemy_language = AlchemyLanguageV1(api_key=ALCHEMY_LANGUAGE_KEY)

"""
    watsonCall makes the call to the AlchemyLanguage API and returns the data requested.
    It is a combined call which keeps the number of requests to Watson to a minimum.
    The data requested resides in the 'extract' field.
    @param link: the link to the article
    
    TODO: look into allowing multiple concept and keyword calls.  I am not sure how the max_item parameter works in combined calls
          Could also look into the effects of having it the default amount.  Refer to relation doc for issues on that
"""
def watsonCall(link):
    response = json.dumps(alchemy_language.combined(url=link, extract='relations, authors', max_items=1), indent=2)
    return json.loads(response)

    
"""
    This block of code traverses the dictionary that the relations call returns from Watson.
    This will give a subject, action, and object of an individual claim as well as the claim itself.
    @param subject: the noun of the claim that is performing the action
    @param object: the noun of the claim that is being acted upon
    @param action: the verb of the claim that the subject is using on the object
    @param sentence: the entire sentence that the claim is made within
    
    TODO: Need to find a way to get more than one claim from a single article
    TODO: Potentially less arbitrary commenting
"""
#sets info to the relation
info = watsonCall(link)

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

# object, sentence, action, and subject are now all set to their respective variables

"""
    This gets the authors from the article
    @param authors: the one or more authors of the article

    TODO: test with multiple authors (should work but who knows)
"""

authors = []

for i in info.items():
    for j in i:
        if (isinstance(j, dict)):
            for k in j.items():
                for l in k:
                    if (isinstance(l, list)):
                        authors = l[:]
