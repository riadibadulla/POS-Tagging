from nltk.corpus import brown
from nltk import FreqDist, WittenBellProbDist
import os
os.system('clear')

def show_sent(sent):
    print(sent)

sentence = brown.tagged_sents(tagset='universal')
emitted = sentence[0]
tags = [t for (_,t) in emitted]

tagsTupples = []

for i in range(len(tags)-1):
    tagsTupples.append((tags[i],tags[i+1]))


tags = set(tags)
smoothed = {}
for tag in tags:
    words = [w for (w,t) in emitted if t == tag]
    smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
#print('prob of N -> Det',smoothed['DET'].prob('NOUN'))
print('prob of N -> The is',smoothed['DET'].prob('The'))
print('prob of N -> Jury is',smoothed['NOUN'].prob('Jury'))
print('prob of N -> said is',smoothed['VERB'].prob('said'))

smoothed = {}
for tag in tags:
    print(tag)
    words = [w for (t,w) in tagsTupples if t == tag]
    smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
print('prob of N -> Det',smoothed['DET'].prob('NOUN'))