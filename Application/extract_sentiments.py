import spacy
from collections import Counter
nlp = spacy.load("en_core_web_lg")
print("Spacy loaded")

entertainment = "I still have to watch Bumblebee Itas reboot of the Transformers franchise which be huge part of my childhood and the design of the classic Transformers in the film look too good to have miss I donat even care if itas bad I have to see it at some point"
doc1 = nlp("%s" % entertainment)
doc2 = [
"Intense",
"Emotional",
"Inspiring",
"Dissapointing",
"Uplifting",
"Cringe",
"Thrilling",
"Memories",
"Refreshing",
"Intelligent",
"Visual",
"Despair",
"Hilarious",
"Comedy",
"Family",
"Exciting",
"High Quality",
"Adorable",
"Depressing",
"Admiration",
"Adoration",
"Aesthetic Appreciation",
"Disgusting",
"Apathy",
"Awkard",
"Confusing",
"Enthralling",
"Empathetic",
"Joy",
"Satisfying",
"Triumphant"
]

nlp_doc2=[]
for sentiment in doc2:
    nlp_doc2.append(nlp(sentiment))

sentiment_value = {}
for sentiment in nlp_doc2:
    sentiment_value.update({sentiment:doc1.similarity(sentiment)})

topSentiments = Counter(sentiment_value)
high = topSentiments.most_common(5)

for i in high:
    print(('{} : {}').format(i[0],i[1]))

