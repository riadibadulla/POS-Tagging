class FBTagger:

    tagsPossible = []
    forwardProbabilities = []
    backwardProbabilities = []
    probability = None
    sentance = []
    resultingTag = []

    def getSumForwardProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            viterbiOfPrevious = self.forwardProbabilities[self.tagsPossible.index(tag)][wordIndex-1]
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
        sumation = sum(listOfPossibleViterbiProb)
        return sumation

    def getSumBackProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            probabilitiesOfNext = self.backwardProbabilities[self.tagsPossible.index(tag)][len(self.sentance) - wordIndex - 2]
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(probabilitiesOfNext*emissionProbability*transitionalProbability)
        sumation = sum(listOfPossibleViterbiProb)
        return sumation

    def __init__(self, probability):
        self.forwardProbabilities = []
        self.sentance = []
        self.resultingTag = []

        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        self.probability = probability
        
    def makeForward(self):
        for tag in self.tagsPossible:
            self.forwardProbabilities.append([self.probability.getTransitionProbability(tag,'<s>')*self.probability.getEmissionProbability(self.sentance[0],tag)])

        for w in range(1,len(self.sentance)):
            for t in range(len(self.tagsPossible)):
                sumationOfPaths = self.getSumForwardProbabilityForState(t,w)
                self.forwardProbabilities[t].append(sumationOfPaths)

        finalisation = []
        for t in range(len(self.tagsPossible)):
            viterbiOfPrevious = self.forwardProbabilities[t][len(self.sentance)-1]
            transitionProbability = self.probability.getTransitionProbability('</s>', self.tagsPossible[t])
            finalisation.append(viterbiOfPrevious*transitionProbability)
        for t in range(len(self.tagsPossible)):
            self.forwardProbabilities[t].append(sum(finalisation))

    
    def makeBackward(self):
        for tag in self.tagsPossible:
            self.backwardProbabilities.append([self.probability.getTransitionProbability('</s>', tag)*self.probability.getEmissionProbability(self.sentance[-1],tag)])

        for w in list(reversed(range(0,len(self.sentance)-1))):
            for t in range(len(self.tagsPossible)):
                sumationOfPaths = self.getSumBackProbabilityForState(t,w)
                self.backwardProbabilities[t].append(sumationOfPaths)

        finalisation = []
        for t in range(len(self.tagsPossible)):
            probabilityOfNext = self.backwardProbabilities[t][0]
            transitionProbability = self.probability.getTransitionProbability(self.tagsPossible[t], '<s>')
            finalisation.append(probabilityOfNext*transitionProbability)
        for t in range(len(self.tagsPossible)):
            self.backwardProbabilities[t].append(sum(finalisation))
        
        for t in range(len(self.tagsPossible)):
            self.backwardProbabilities[t] = list(reversed(self.backwardProbabilities[t]))

    def tagTheSentance(self,sentance):
        self.sentance = sentance
        self.makeForward()
        self.makeBackward()
        self.resultingTag.append('<s>')
        for w in range(len(sentance)):
            tagProbabilities = []
            for t in range(len(self.tagsPossible)):
                transitionPr = self.probability.getTransitionProbability(self.tagsPossible[t], self.resultingTag[-1])
                emissionPr = self.probability.getEmissionProbability(sentance[w],self.tagsPossible[t])
                tagProbability = self.forwardProbabilities[t][w]*self.backwardProbabilities[self.tagsPossible.index(self.resultingTag[-1])][w]*transitionPr*emissionPr
                tagProbabilities.append(tagProbability)
            maximumProbabilityForTheWord = max(tagProbabilities)
            indexOfMaximumProbability = tagProbabilities.index(maximumProbabilityForTheWord)
            self.resultingTag.append(self.tagsPossible[indexOfMaximumProbability])
        self.resultingTag.remove('<s>')
        return(self.resultingTag)

