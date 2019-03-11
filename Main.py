import os
import Probabilities
import ViterbiTagging
import EagerTagging
from nltk.corpus import brown
os.system('clear')

probability = Probabilities.Probabilities()
sentences = brown.tagged_sents(tagset='universal')

def getAccuracy(originalTags, predictedTags):
    numberOfWords = len(originalTags)
    numberOfRughtPrediction = 0

    for i in range(numberOfWords):
        if (originalTags[i] == predictedTags[i]):
            numberOfRughtPrediction+=1
    return numberOfRughtPrediction/numberOfWords

def testViterbi():
    allTagsPredcited = []
    tagsFromCorpus = []
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        viterbi = ViterbiTagging.ViterbiTagger(probability)
        tagsPredicted = viterbi.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        #accuracyCurrent = getAccuracy(tags, tagsPredicted)
        #if (accuracyCurrent < 0.9):
         #   print(i,"  ",accuracyCurrent)
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("viterbi ",getAccuracy(tagsFromCorpus,allTagsPredcited))

#53010 was underflow

def testEager():
    allTagsPredcited = []
    tagsFromCorpus = []   
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        eager = EagerTagging.Eager(probability, 1)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("eager ",getAccuracy(tagsFromCorpus,allTagsPredcited))


def compareAlgorithms():
    for i in range(10257,10258):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        viterbi = ViterbiTagging.ViterbiTagger(probability)
        tagsPredicted = viterbi.tagTheSentance(onlyWords)
        #print(onlyWords)
        #print(tagsPredicted)
        #print(tags)
        viterbiaAc = getAccuracy(tags,tagsPredicted)
        eager = EagerTagging.Eager(probability, 1)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        eagAc = getAccuracy(tags,tagsPredicted)
        if viterbiaAc < eagAc:
            print(i)

#compareAlgorithms()

testViterbi()
testEager()


# onlyWords = [w for (w,t) in sentences[10257]]
# tags = [t for (w,t) in sentences[10257]]
# viterbi = ViterbiTagging.ViterbiTagger(probability)
# tagsPredicted = viterbi.tagTheSentance(onlyWords)
# print(onlyWords)
# print(tagsPredicted)
# print(tags)
# print(getAccuracy(tags,tagsPredicted))