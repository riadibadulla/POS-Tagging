
class ViterbiTagger:

    tagsPossible = []
    viterbi = []
    probability = None
    sentance = []
    backpointer = []

    def printEmissionProbabilities(self, sentence):
        possibleTags = self.probability.uniqueTags
        words = [w for (w,_) in sentence]
        for word in words:    
            for tag in possibleTags:
                print("P(",word,"|",tag,") = ",self.probability.getEmissionProbability(word,tag))

    def printTransitionProbabilities(self, probability):
        possibleTags = probability.uniqueTags
        for tag in possibleTags:    
            for givenTag in possibleTags:
                print("P(",tag,"|",givenTag,") = ",self.probability.getTransitionProbability(tag,givenTag))

    def getMaxViterbiProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            viterbiOfPrevious = self.viterbi[self.tagsPossible.index(tag)][wordIndex-1]
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
        maximumValue = max(listOfPossibleViterbiProb)
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])
    
    def __init__(self, probability, sentance):
        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        self.probability = probability
        self.sentance = sentance

        for tag in self.tagsPossible:
            self.viterbi.append([probability.getTransitionProbability(tag,'<s>')*probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append(['<s>'])

        for w in range(1,len(sentance)):
            for t in range(len(self.tagsPossible)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer[t].append(maximumViterbi[1])

        endProbability = 0
        for t in range(len(self.tagsPossible)):
            viterbiOfPrevious = self.viterbi[t][len(sentance)-1]
            transitionProbability = self.probability.getTransitionProbability('</s>', self.tagsPossible[t])
            if (viterbiOfPrevious*transitionProbability > endProbability):
                endProbability = viterbiOfPrevious*transitionProbability
                self.backpointer[:].append(self.tagsPossible[t])



        print(sentance)
        print(probability.uniqueTags)