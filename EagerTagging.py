class Eager:
    tagsPossible = []
    viterbi = []
    probability = None
    sentance = []
    backpointer = []
    resultingTag = []
    K = 1
    fail = False

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
            if (self.viterbi[self.tagsPossible.index(tag)][wordIndex-1] != 0):
                viterbiOfPrevious = self.viterbi[self.tagsPossible.index(tag)][wordIndex-1]
                emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
                transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
                listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
        try:
            maximumValue = max(listOfPossibleViterbiProb)
        except:
            self.fail = True
            return (0, 'Underflow')    
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])

    def recursive(self,tag, i):
        if (i > 0):
            self.resultingTag.append(self.backpointer[self.tagsPossible.index(tag)][i])
            self.recursive(self.backpointer[self.tagsPossible.index(tag)][i-1],i-1)
        else:
            return -1

    def getTags(self,lastTag):
        self.resultingTag.append(lastTag)
        self.recursive(lastTag, len(self.backpointer[0])-1)

    def keepMaximum(self, wordIndex):
        maximumTagsFound = []
        column = [v[wordIndex] for v in self.viterbi]
        for i in range(self.K):
            maxim = max(column)
            maximumTagsFound.append([row[wordIndex] for row in self.viterbi].index(maxim))
            column.remove(maxim)
        
        for i in range(len(self.viterbi)):
            if i not in maximumTagsFound:
                self.viterbi[i][wordIndex] = 0

    def __init__(self, probability, K):
        self.viterbi = []
        self.sentance = []
        self.backpointer = []
        self.resultingTag = []
        self.K = K
        self.fail = False

        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        self.tagsPossible.remove('<s>')
        self.probability = probability
        
    
    def tagTheSentance(self, sentance):
        self.sentance = sentance

        for tag in self.tagsPossible:
            self.viterbi.append([self.probability.getTransitionProbability(tag,'<s>')*self.probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append(['<s>'])

        self.keepMaximum(0)

        for w in range(1,len(sentance)):
            for t in range(len(self.tagsPossible)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                if self.fail == True:
                    return []
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer[t].append(maximumViterbi[1])
            self.keepMaximum(w)


        endProbability = 0
        lasTag = ''
        for t in range(len(self.tagsPossible)):
            viterbiOfPrevious = self.viterbi[t][len(sentance)-1]
            transitionProbability = self.probability.getTransitionProbability('</s>', self.tagsPossible[t])
            if (viterbiOfPrevious*transitionProbability > endProbability):
                endProbability = viterbiOfPrevious*transitionProbability
                lasTag = self.tagsPossible[t]
        
        if (lasTag != ''):
            self.getTags(lasTag)
        else:
            return []
        return list(reversed(self.resultingTag))

  