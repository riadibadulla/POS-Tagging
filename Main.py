

import os
import Probabilities
os.system('clear')

probability = Probabilities.Probabilities()

print(probability.getEmissionProbability("The","DET"))
print(probability.getTransitionProbability("VERB","DET"))


