import os
import Probabilities
import ViterbiTagging
import BeamSearch
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
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("Viterbi Accuracy ",getAccuracy(tagsFromCorpus,allTagsPredcited))

#53010 gives underflow

def testBeam(K):
    allTagsPredcited = []
    tagsFromCorpus = []
    tagsPredicted = []
    for i in range(10000,10500):
        onlyWords = [w for (w,t) in sentences[i]]
        tags = [t for (w,t) in sentences[i]]
        beam = BeamSearch.Beam(probability, K)
        tagsPredicted = beam.tagTheSentance(onlyWords)
        if (tagsPredicted == []):
            print(i," is underflow")    
            continue
        allTagsPredcited.extend(tagsPredicted[:])
        tagsFromCorpus.extend(tags[:])
    print("beam K=(",K,") Accuracy: ",getAccuracy(tagsFromCorpus,allTagsPredcited))

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
    print("Forward Backward Accuracy: ",getAccuracy(tagsFromCorpus,allTagsPredcited))


testViterbi()
testBeam(1) #Maximum 13, which makes it Viterbi
testBeam(2) #Maximum 13, which makes it Viterbi
testFB()
