import os
import Probabilities
import ViterbiTagging
import EagerTagging
from nltk.corpus import brown
os.system('clear')


def getAccuracy(originalSentence, predictedTags):
    numberOfWords = len(originalSentence)
    originalTags = [t for (w,t) in originalSentence]
    numberOfRughtPrediction = 0

    for i in range(numberOfWords):
        if (originalTags[i] == predictedTags[i]):
            numberOfRughtPrediction+=1
    return numberOfRughtPrediction/numberOfWords


probability = Probabilities.Probabilities()
sentences = brown.tagged_sents(tagset='universal')

def testViterbi():
    arrayOfAccuracies = []    
    for i in range(51605,len(sentences)-1):
        onlyWords = [w for (w,t) in sentences[i]]
        viterbi = ViterbiTagging.ViterbiTagger(probability)
        tagsPredicted = viterbi.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        arrayOfAccuracies.append(getAccuracy(sentences[i],tagsPredicted))
    print(sum(arrayOfAccuracies)/len(arrayOfAccuracies))


#53010 was underflow
#testViterbi()


#onlyWords = ['The', 'purge', 'has', 'taken' '.']
# onlyWords = [w for (w,t) in sentences[5020]]
# print([t for (w,t) in sentences[5020]])
# eager = EagerTagging.Eager(probability, 2)
# tagsPredicted = eager.tagTheSentance(onlyWords)
# print(tagsPredicted)

def testEager():
    arrayOfAccuracies = []    
    for i in range(51605,len(sentences)-1):
        onlyWords = [w for (w,t) in sentences[i]]
        eager = EagerTagging.Eager(probability, 1)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        arrayOfAccuracies.append(getAccuracy(sentences[i],tagsPredicted))
    print(sum(arrayOfAccuracies)/len(arrayOfAccuracies))

testEager()