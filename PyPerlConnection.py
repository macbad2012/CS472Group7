#When finished, this code should be copied into the main program, and modified as necessary
import subprocess

url = "facebook.com" #can be full url
pathToPerlScript ='C:/Users/Stephen/Downloads/CS472Group7-master/CS472Group7-master' #CHANGE THIS!
pipe = subprocess.Popen(["perl", "wot.pl",url, pathToPerlScript], stdout=subprocess.PIPE)
perl_stdout = pipe.communicate(input=pathToPerlScript)
responce = perl_stdout[0].decode().replace('\r','').split('\n')
print(responce)