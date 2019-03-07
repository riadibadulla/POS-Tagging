import os
import Probabilities
import ViterbiTagging
from nltk.corpus import brown
os.system('clear')

probability = Probabilities.Probabilities()

sentences = brown.tagged_sents(tagset='universal')
#print(probability.getEmissionProbability("game","NOUN"))
#print(probability.getTransitionProbability("NOUN","DET"))

#print(sentences[51605])
onlyWords = [w for (w,t) in sentences[51605][0:5]]

#ViterbiTagging.printEmissionProbabilities(probability,sentences[51605][0:5])
#ViterbiTagging.printTransitionProbabilities(probability)
viterbi = ViterbiTagging.ViterbiTagger(probability,onlyWords)

