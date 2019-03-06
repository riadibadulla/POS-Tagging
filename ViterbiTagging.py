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