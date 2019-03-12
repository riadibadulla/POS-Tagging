class ViterbiTagger:

    tagsPossible = []   #unique taglist, list of all possible tags
    viterbi = []        #viterbiMatrix
    probability = None  #probability Object, which stores all emission an transition probabilities
    sentance = []       #sentance to tag, contains only words
    backpointer = []    #extension of viterbi matrix, contains best tags from which it came to this word's tag
    resultingTag = []   #result which needs to be return, eventually will contain all tags for the sentence

    """Calculate viterbi for each word and possible tag
        Returns tuple of value for the cell and tag, where it came from
    """
    def getMaxViterbiProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:
            viterbiOfPrevious = self.viterbi[self.tagsPossible.index(tag)][wordIndex-1]
            emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
            transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
            listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
        
        #Get the maximum of possible combinations
        maximumValue = max(listOfPossibleViterbiProb)
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])

    """Recursively get tags using backtracking in backpointer"""
    def recursive(self,tag, i):
        if (i > 0):
            tag = self.backpointer[self.tagsPossible.index(tag)][i]
            self.resultingTag.append(tag)
            self.recursive(tag,i-1)
        else:
            return -1

    """Calls recursive function, to get tags"""
    def getTags(self,lastTag):
        self.resultingTag.append(lastTag)
        self.recursive(lastTag, len(self.backpointer[0])-1)

    """ Initialiser, resets all class"""
    def __init__(self, probability):
        self.viterbi = []
        self.sentance = []
        self.backpointer = []
        self.resultingTag = []

        self.tagsPossible = list(probability.uniqueTags)
        self.tagsPossible.remove('</s>')
        self.probability = probability
        
    """The main tagger"""
    def tagTheSentance(self, sentance):
        self.sentance = sentance

        #Initialise
        for tag in self.tagsPossible:
            self.viterbi.append([self.probability.getTransitionProbability(tag,'<s>')*self.probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append(['<s>'])

        #Recursive part
        for w in range(1,len(sentance)):
            for t in range(len(self.tagsPossible)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer[t].append(maximumViterbi[1])

        #Get last tag
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

