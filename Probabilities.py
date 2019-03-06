from nltk.corpus import brown
from nltk import FreqDist, WittenBellProbDist
class Probabilities:
    
    emitted = []
    tags = []
    tagsTupples = []
    uniqieTags = []
    allWords = []

    emissionProbability = {}
    transitionProbability = {}

    def show_sent(self, sent):
        print(sent)

    def __init__(self):
        sentence = brown.tagged_sents(tagset='universal')[0]
        self.allWords = [w for (w,_) in sentence]
        self.emitted = sentence[0]
        self.tags = [t for (_,t) in self.emitted]
        for i in range(len(self.tags)-1):
            self.tagsTupples.append((self.tags[i],self.tags[i+1]))
        uniqieTags = set(tags)
    
    
    def createEmissionProbabilities(self):
        smoothed = {}
        words = []
        for tag in uniquesTags:
            words = [w for (w,t) in emitted if t == tag]
            smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
        emissionProbability = smoothed
        return smoothed

    def createTransitionProbabilities(self):
        smoothed = {}
        for tag in tags:
            print(tag)
            words = [w for (t,w) in tagsTupples if t == tag]
            smoothed[tag] = WittenBellProbDist(FreqDist(words), bins=1e5)
        print('prob of N -> Det',smoothed['DET'].prob('NOUN'))
        transitionProbability = smoothed
        return smoothed