import os
import Probabilities
from nltk.corpus import brown
os.system('clear')

probability = Probabilities.Probabilities()

sentence = brown.tagged_sents(tagset='universal')

#self.allWords = [w for (w,_) in self.emitted]
#print(len(sentence))

print(probability.getEmissionProbability("Georgia","NOUN"))
print(probability.getTransitionProbability("NOUN","DET"))


