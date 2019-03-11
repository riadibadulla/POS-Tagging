class Eager:
    tagsPossible = []
    viterbi = []
    probability = None
    sentance = []
    backpointer = []
    resultingTag = []
    K = 1
    fail = False

    def getMaxViterbiProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            if (self.viterbi[self.tagsPossible.index(tag)][wordIndex-1] != -1):
                viterbiOfPrevious = self.viterbi[self.tagsPossible.index(tag)][wordIndex-1]
                emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
                transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
                listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
            else:
                listOfPossibleViterbiProb.append(-1)
        try:
            maximumValue = max(listOfPossibleViterbiProb)
        except:
            self.fail = True
            return (0, 'Underflow')    
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])

    def recursive(self,tag, i):
        if (i<=0):
            return True
        if (i > 0):
            tag = self.backpointer[self.tagsPossible.index(tag)][i]
            if (len(self.resultingTag)) != (len(self.sentance)):
                self.resultingTag.append(tag)
                self.recursive(tag,i-1)

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
                self.viterbi[i][wordIndex] = -1
                self.backpointer[i][wordIndex] = ''

    def __init__(self, probability, K):
        self.viterbi = []
        self.sentance = []
        self.backpointer = []
        self.resultingTag = []
        self.K = K
        self.fail = False
        self.tagsPossible =[]
        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        #self.tagsPossible.remove('<s>')
        self.probability = probability
        
    
    # def getLastTag(self, sentance):
    #     listOfProbabilities = []
    #     for t in range(len(self.tagsPossible)):
            
    #             viterbiOfPrevious = self.viterbi[t][len(sentance)-1]
    #             transitionProbability = self.probability.getTransitionProbability('</s>', self.tagsPossible[t])
    #             prob = viterbiOfPrevious*transitionProbability
    #             listOfProbabilities.append(prob)
    #         else:
    #             listOfProbabilities.append(-1)
    #     try:
    #         maximumValue = max(listOfProbabilities)
    #     except:
    #         self.fail = True
    #         return (0, 'Underflow')    
    #     IndexOfMaximum = listOfProbabilities.index(maximumValue)
    #     return self.tagsPossible[IndexOfMaximum]
    
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


        #lasTag = self.getLastTag(sentance)
        endProbability = 0
        lasTag = ''
        for t in range(len(self.tagsPossible)):
            if (self.viterbi[t][len(sentance)-1] != -1):
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

  