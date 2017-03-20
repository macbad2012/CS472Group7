#!/usr/bin/python3
"""
    This script calls the Watson Alchemy Language API and the Web of Trust API
    It currently parses the data that is most valuable for identifying the context of a source and places it into
        a list for easy access
    This script will be called by the web server and the data will be used for comparison and evaluation of the credibility of the source
    
    As the current time the response is only printed
"""





"""
    argv pulls the command line arguments
    AlchemyLanguageV1 is the reference to Watson's API
    json allows for easy access to the returned data from Watson
    re is regex which is used to parse the desired info from the Watson data
    subprocess: ?
"""
from watson_developer_cloud import AlchemyLanguageV1
import json
import re
import subprocess
import cgitb; cgitb.enable()
import cgi

input_data  = cgi.FieldStorage()

link = input_data


#These are the API key and the reference to Watson's Alchemy Language
ALCHEMY_LANGUAGE_KEY = "c251be18000cca3f91ffcdf95b9ae67c5b8f6ef1"
alchemy_language = AlchemyLanguageV1(api_key=ALCHEMY_LANGUAGE_KEY)

"""
    watsonCall makes the call to the AlchemyLanguage API and returns the data requested.
    It is a combined call which keeps the number of requests to Watson to a minimum.
    The data requested resides in the 'extract' field.
    @param link: the link to the article
"""
def watsonCall(link):
    response = json.dumps(alchemy_language.combined(url=link, extract='relations, authors, keywords, doc-emotion', max_items=1), indent=2)
    return json.loads(response)


"""
    This block of code traverses the dictionary that the relations call returns from Watson.
    This will give a subject, action, and object of an individual claim as well as the claim itself.
    @param subject: the noun of the claim that is performing the action
    @param object: the noun of the claim that is being acted upon
    @param action: the verb of the claim that the subject is using on the object
    @param sentence: the entire sentence that the claim is made within
    
    TODO: Potentially less arbitrary commenting
"""
#sets info to the relation
info = watsonCall(link)
infoStr = str(info)

relations = [] 

SENTENCE_PATTERN = "'sentence': [\"'](.*?)[\"']"
SUBJECT_PATTERN = "'subject': .*?'text': '(.*?)'"
OBJECT_PATTERN = "'object': .*?'text': '(.*?)'"
ACTION_PATTERN = "'lemmatized': '(.*?)'"

sentence = []
subject = []
obj = []
action = []

sentenceMatch = re.findall(SENTENCE_PATTERN, infoStr)
subjectMatch = re.findall(SUBJECT_PATTERN, infoStr)
objectMatch = re.findall(OBJECT_PATTERN, infoStr)
actionMatch = re.findall(ACTION_PATTERN, infoStr)

for i in sentenceMatch:
    sentence.append(i)
for i in subjectMatch:
    subject.append(i)
for i in objectMatch:
    obj.append(i)
for i in actionMatch:
    action.append(i)

numOfMatches = len(sentence)
for i in range(0, numOfMatches):
    tempDict = {'object': obj[i], 'sentence': sentence[i], 'action': action[i], 'subject': subject[i]}
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

watsonResp = [relations, authors, keywords]


"""
    Calls the Web Of Trust code and returns the response to the variable 'wot'
    @param pathToPerlScript: the file system path to the location of the web of trust perl script
    @param pipe: the reference to the perl script
    @param perl_stdout: the call to the perl script that gets the coded reponse
    @param wot: the parameter that holds the Web of Trust response
"""
#TODO: change the path to the perl script
pathToPerlScript ='/PATH/TO/PERL/SCRIPT' 
pipe = subprocess.Popen(["perl", "wot.pl", link, pathToPerlScript], stdout=subprocess.PIPE)
perl_stdout = pipe.communicate(input=pathToPerlScript)
wot = perl_stdout[0].decode().replace('\r','').split('\n')

fullResponse = [watsonResp, wot]
print ("Content-type: text/html")
print(fullResponse);
