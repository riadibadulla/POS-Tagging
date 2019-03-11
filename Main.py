import os
import Probabilities
import ViterbiTagging
import EagerTagging
import ForwardBackward
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
    tagsPredicted = []
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        eager = EagerTagging.Eager(probability, 13)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("eager ",getAccuracy(tagsFromCorpus,allTagsPredcited))

def testFB():
    allTagsPredcited = []
    tagsFromCorpus = []   
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        forward = ForwardBackward.FBTagger(probability)
        tagsPredicted = forward.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("FB ",getAccuracy(tagsFromCorpus,allTagsPredcited))

def compareAlgorithms():
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        viterbi = ViterbiTagging.ViterbiTagger(probability)
        tagsPredicted = viterbi.tagTheSentance(onlyWords)
        #print(onlyWords)
        #print(tagsPredicted)
        #print(tags)
        viterbiaAc = getAccuracy(tags,tagsPredicted)
        eager = EagerTagging.Eager(probability, 13)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        eagAc = getAccuracy(tags,tagsPredicted)
        print(viterbiaAc,'  ',eagAc)
        print(i)
        print(' ')

#compareAlgorithms()

#testViterbi()
testEager()
#testFB()
