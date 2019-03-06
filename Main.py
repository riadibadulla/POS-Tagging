import os
import Probabilities
from nltk.corpus import brown
os.system('clear')

probability = Probabilities.Probabilities()

sentence = brown.tagged_sents(tagset='universal')

#self.allWords = [w for (w,_) in self.emitted]
print(sentence[51605])

#print(probability.getEmissionProbability("game","NOUN"))
#print(probability.getTransitionProbability("NOUN","DET"))

import ViterbiTagging
#ViterbiTagging.printEmissionProbabilities(probability,sentence[51605])
ViterbiTagging.printTransitionProbabilities(probability)

