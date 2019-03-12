class Beam:
   
    tagsPossible = []   #unique taglist, list of all possible tags
    viterbi = []        #viterbiMatrix
    probability = None  #probability Object, which stores all emission an transition probabilities
    sentance = []       #sentance to tag, contains only words
    backpointer = []    #extension of viterbi matrix, contains best tags from which it came to this word's tag
    resultingTag = []   #result which needs to be return, eventually will contain all tags for the sentence
    K = 1               #Width of the beam search
    fail = False        #True If the underflow happens. False if the algorithm is succesful

    """Calculate viterbi for each word and possible tag
        Returns tuple of value for the cell and tag, where it came from
    """
    def getMaxViterbiProbabilityForState(self, tagIndex, wordIndex):
        listOfPossibleViterbiProb = []
        for tag in self.tagsPossible:

            #As soon as non maximum values from the previous column are set to -1, we ignore them
            if (self.viterbi[self.tagsPossible.index(tag)][wordIndex-1] != -1):
                viterbiOfPrevious = self.viterbi[self.tagsPossible.index(tag)][wordIndex-1]
                emissionProbability = self.probability.getEmissionProbability(self.sentance[wordIndex],self.tagsPossible[tagIndex])
                transitionalProbability = self.probability.getTransitionProbability(self.tagsPossible[tagIndex], tag)
                listOfPossibleViterbiProb.append(viterbiOfPrevious*emissionProbability*transitionalProbability)
            else:
                listOfPossibleViterbiProb.append(-1)
        
        #Get the maximum of possible combinations
        try:
            maximumValue = max(listOfPossibleViterbiProb)
        except:
            self.fail = True
            return (0, 'Underflow')

        #index Of Best tag    
        IndexOfMaximum = listOfPossibleViterbiProb.index(maximumValue)
        return (maximumValue, self.tagsPossible[IndexOfMaximum])

    """Recursively get tags using backtracking in backpointer"""
    def recursive(self,tag, i):
        if (i<=0):
            return True
        if (i > 0):
            tag = self.backpointer[self.tagsPossible.index(tag)][i]
            if (len(self.resultingTag)) != (len(self.sentance)):
                self.resultingTag.append(tag)
                self.recursive(tag,i-1)

    """Calls recursive function, to get tags"""
    def getTags(self,lastTag):
        self.resultingTag.append(lastTag)
        self.recursive(lastTag, len(self.backpointer[0])-1)

    """keep K maximum values for each column in beam search"""
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

    """ Initialiser, resets all class"""
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
        self.probability = probability
    
    """The main tagger"""
    def tagTheSentance(self, sentance):
        self.sentance = sentance

        #Initialise
        for tag in self.tagsPossible:
            self.viterbi.append([self.probability.getTransitionProbability(tag,'<s>')*self.probability.getEmissionProbability(sentance[0],tag)])
            self.backpointer.append(['<s>'])
        
        #Keep maximum, depending on width
        self.keepMaximum(0)

        #Recursive part
        for w in range(1,len(sentance)):
            for t in range(len(self.tagsPossible)):
                maximumViterbi = self.getMaxViterbiProbabilityForState(t,w)
                
                #Underflow check
                if self.fail == True:
                    return []
                self.viterbi[t].append(maximumViterbi[0])
                self.backpointer[t].append(maximumViterbi[1])
            self.keepMaximum(w)

        #Get last tag
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

  