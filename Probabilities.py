from nltk.corpus import brown
from nltk import FreqDist, WittenBellProbDist
import numpy as np

class Probabilities:
    
    emitted = []
    tags = []
    tagsTupples = []
    uniqueTags = []
    allWords = []

    emissionProbability = {}
    transitionProbability = {}

    def show_sent(self, sent):
        print(sent)

    def createEmissionProbabilities(self):
        smoothed = {}
        words = []
        for tag in self.uniqueTags:
            words = [w for (w,t) in self.emitted if t == tag]
            smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
        self.emissionProbability = smoothed

    def createTransitionProbabilities(self):
        smoothed = {}
        
        #In fact words here are tags
        for tag in self.uniqueTags:
            words = [w for (t,w) in self.tagsTupples if t == tag]
            smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
        self.transitionProbability = smoothed

    """make all in 1d array, and and start and end of sentence."""
    def reshapeTheList(self, array):
        resultingArray = []
        for sentence in array:
            resultingArray.append(tuple(['SOS','<s>']))
            for word in sentence:
                resultingArray.append(word)
            resultingArray.append(tuple(['EOS','</s>']))
        return resultingArray

    """make bigrams"""
    def makeListOfTupplesOfTags(self, tagsList):
        for i in range(len(tagsList)-1):
            if (tagsList[i] != '</s>'):
                self.tagsTupples.append((tagsList[i],tagsList[i+1]))

    def __init__(self):
        sentence = brown.tagged_sents(tagset='universal')
        #self.emitted = sentence[0:51605]
        self.emitted = sentence[0:10000]
        self.emitted = self.reshapeTheList(self.emitted)

        self.allWords = [w for (w,_) in self.emitted]
        self.tags = [t for (_,t) in self.emitted]
        self.makeListOfTupplesOfTags(self.tags)

        self.uniqueTags = set(self.tags)

        self.createEmissionProbabilities()
        self.createTransitionProbabilities()
    
    def getEmissionProbability(self,word, tag):
        return self.emissionProbability[tag].prob(word)
    
    def getTransitionProbability(self,tag, previousTag):
        return self.transitionProbability[previousTag].prob(tag)