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

    for i in range(numberOfWords-1):
        if (originalTags[i] == predictedTags[i]):
            numberOfRughtPrediction+=1
    return numberOfRughtPrediction/numberOfWords


probability = Probabilities.Probabilities()
sentences = brown.tagged_sents(tagset='universal')

def testViterbi():
    for i in range(51605,len(sentences)-1):
        onlyWords = [w for (w,t) in sentences[i]]
        viterbi = ViterbiTagging.ViterbiTagger(probability)
        tagsPredicted = viterbi.tagTheSentance(onlyWords)
        del viterbi
        print(getAccuracy(sentences[i],tagsPredicted))

#testViterbi()

def testEager():
    for i in range(51605,len(sentences)-1):
        onlyWords = [w for (w,t) in sentences[i]]
        eager = EagerTagging.Eager(probability)
        tagsPredicted = eager.tagTheSentance(onlyWords)
        del eager
        print(getAccuracy(sentences[i],tagsPredicted))

#testEager()

onlyWords = [w for (w,t) in sentences[5500]]
print(sentences[5500][0:3])
eager = ViterbiTagging.ViterbiTagger(probability)
tagsPredicted = eager.tagTheSentance(onlyWords)
print(tagsPredicted)
