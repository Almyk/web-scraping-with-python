from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, string, operator
import itertools
from collections import OrderedDict

n = 2

commonWords = []
f = open("commonWords.txt", 'r')
for line in f:
    commonWords.append(line.strip())
f.close()

def isCommon(ngram):
    global commonWords
    words = ngram.split(" ")
    for word in words:
        if word.lower() in commonWords:
            return True
    return False

def cleanInput(input):
    input = re.sub('\n+', " ", input).lower()
    input = re.sub('\[[0-9]\]', "", input) # removes strings of the pattern: [2343]
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
        ngramTemp = " ".join(input[i:i+n])
        if (isCommon(ngramTemp)):
            continue
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

content = str(\
        urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
allSentences = content.split(".")
ngrams = ngrams(content, n)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)
top5 = list(itertools.islice(sortedNGrams, 5))
#print(sortedNGrams)
#print(top5)

selectedNgrams = []
for x,y in top5:
    selectedNgrams.append(x)

selectedSentences = []
for ngram in selectedNgrams:
    for sentence in allSentences:
        if ngram.lower() in sentence.lower():
            selectedSentences.append(sentence)
            break
        

for sentence in selectedSentences:
    print(sentence.strip()+".\n")
