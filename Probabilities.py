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
        for tag in self.tags:
            words = [w for (t,w) in self.tagsTupples if t == tag]
            smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
        self.transitionProbability = smoothed

    def __init__(self):
        sentence = brown.tagged_sents(tagset='universal')
        self.emitted = sentence[0:2500]
        mitted = np.asarray(self.emitted).reshape(-1).tolist()

        self.allWords = [w for (w,_) in self.emitted]
        self.tags = [t for (_,t) in self.emitted]
        for i in range(len(self.tags)-1):
            self.tagsTupples.append((self.tags[i],self.tags[i+1]))
        self.uniqueTags = set(self.tags)

        self.createEmissionProbabilities()
        self.createTransitionProbabilities()
    


    def getEmissionProbability(self,word, tag):
        return self.emissionProbability[tag].prob(word)
    
    def getTransitionProbability(self,tag, previousTag):
        return self.transitionProbability[previousTag].prob(tag)