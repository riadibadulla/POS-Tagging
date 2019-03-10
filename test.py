from nltk.corpus import brown

sentences = brown.tagged_sents(tagset='universal')
print(sentences[5300])