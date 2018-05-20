from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict
from itertools import islice

n = 3

def cleanInput(input):
    input = input.upper()
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)
    output = {} 
    for i in range(len(input)-n+1):
        if str(input[i:i+n]) in output:
            output[str(input[i:i+n])] += 1
        else:
            output[str(input[i:i+n])] = 1
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, "lxml")
content = bsObj.find("div", {"id":"mw-content-text"}).text
ngrams = ngrams(content, n)
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
n_ngrams = islice(ngrams.items(), 0, 20)
print("List of Top 20 %d-grams:"%n)
i = 1
for key, value in n_ngrams:
    print ("#%2d"%i, "%-40s"%key, value)
    i += 1
#print(n_ngrams)
print("%d-grams count is: "%n+str(len(ngrams)))
