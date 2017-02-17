#!/usr/bin/python3.5

from sys import argv
from watson_developer_cloud import AlchemyLanguageV1
import json
import re

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
          max_items=1 is sufficient for my testing purposes but needs to be changed for realistic usage later
"""
def watsonCall(link):
    response = json.dumps(alchemy_language.combined(url=link, extract='relations, authors, keywords', max_items=1), indent=2)
    return json.loads(response)


"""
    This block of code traverses the dictionary that the relations call returns from Watson.
    This will give a subject, action, and object of an individual claim as well as the claim itself.
    @param subject: the noun of the claim that is performing the action
    @param object: the noun of the claim that is being acted upon
    @param action: the verb of the claim that the subject is using on the object
    @param sentence: the entire sentence that the claim is made within
    
    TODO: Need to find a way to get more than one claim from a single article
          Currently the it is setting the variables to the last claim recieved
    TODO: Potentially less arbitrary commenting
"""
#sets info to the relation
info = watsonCall(link)
infoStr = str(info)

relations = [] 

SENTENCE_PATTERN = "'sentence': '(.*?)'"
SUBJECT_PATTERN = "'subject': .*?'text': '(.*?)'"
OBJECT_PATTERN = "'object': .*?'text': '(.*?)'"
ACTION_PATTERN = "'lemmatized': '(.*?)'"

sentenceMatch = re.search(SENTENCE_PATTERN, infoStr)
subjectMatch = re.search(SUBJECT_PATTERN, infoStr)
objectMatch = re.search(OBJECT_PATTERN, infoStr)
actionMatch = re.search(ACTION_PATTERN, infoStr)

sentence = sentenceMatch.group(1)
subject = subjectMatch.group(1)
obj = objectMatch.group(1)
action = actionMatch.group(1)

tempDict = {'object': obj, 'sentence': sentence, 'action': action, 'subject': subject}
relations.append(tempDict)

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


"""
    Gets the keywords of the article and places them into a list in descending order of relevance
    @param keywords: the list of keywords in descending order of relevance
"""

keywords = []

for i in info["keywords"]:
    for j in i.items():
        if(j[0] == "text"):
            keywords.append(j[1])

print(relations)
