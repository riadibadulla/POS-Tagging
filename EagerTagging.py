
class Eager:

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
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(emissionProbability*transitionalProbability)
        maximumValue = max(listOfPossibleViterbiProb)
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])
    
    def getTags(self):
        taglist = []
        for i in range(len(self.sentance)):
            maxim = max(v[i] for v in self.viterbi)
            taglist.append(self.backpointer[[row[i] for row in self.viterbi].index(maxim)][i])
        return(taglist)

    def __init__(self, probability):
        self.viterbi = []
        self.sentance = []
        self.backpointer = []

        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        self.probability = probability
        
    
    def tagTheSentance(self, sentance):
        self.sentance = sentance

        for tag in self.tagsPossible:
            self.viterbi.append([self.probability.getTransitionProbability(tag,'<s>')*self.probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append(['<s>'])

        for w in range(1,len(sentance)):
            for t in range(len(self.tagsPossible)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer[t].append(maximumViterbi[1])

        result = self.getTags()
        result.pop(0)
        return result
