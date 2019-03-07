
class ViterbiTagger:

    tagsPossible = []
    viterbi = []
    probability = None
    sentance = []
    backpointer = []

    def printEmissionProbabilities(probability, sentence):
        possibleTags = probability.uniqueTags
        words = [w for (w,_) in sentence]
        for word in words:    
            for tag in possibleTags:
                print("P(",word,"|",tag,") = ",probability.getEmissionProbability(word,tag))

    def printTransitionProbabilities(probability):
        possibleTags = probability.uniqueTags
        for tag in possibleTags:    
            for givenTag in possibleTags:
                print("P(",tag,"|",givenTag,") = ",probability.getTransitionProbability(tag,givenTag))

    def getMaxViterbiProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            viterbiOfPrevious = self.viterbi[tagIndex,wordIndex-1]
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
        maximumValue = max(listOfPossibleViterbiProb)
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, IndexOfMaximum)
    
    def __init__(self, probability, sentance):
        self.tagsPossible = probability.uniqueTags
        self.probability = probability
        self.sentance = sentance

        for tag in self.tagsPossible:
            self.viterbi.append([probability.getTransitionProbability(tag,'<s>')*probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append([])
        for t in range(len(self.tagsPossible)):
            for w in range(1,len(sentance)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer.append[t].append(maximumViterbi[1])

        print(sentance)
        print(probability.uniqueTags)