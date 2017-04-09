import nltk
import wikipedia
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

text = None
with open('review.txt', 'r') as f:
    text = f.read()

def extractEntities(ne_chunked):
	for entity in ne_chunked:
		if isinstance(entity, nltk.tree.Tree):
			text = " ".join([word for word, tag in entity.leaves()])
			ent = entity.label()
			return text;
		else:
			continue
	return "Thing"

wiki = None
def readNltk():
	tfile = open("wiki.txt", "r")
	wiki = tfile.read().split(',')
	return wiki;


wiki2 = None
def readEnt():
	with open("wiki2.txt") as f:
		wiki2 = f.readlines()
	wiki2 = [x.strip('\n') for x in wiki2]	
	print wiki2
	return wiki2;

def findWiki(wiki):
	for word in wiki:
		print(word)
		try:
			page=wikipedia.page(word)
		except wikipedia.exceptions.PageError:
			print "Thing"
			continue
		except wikipedia.exceptions.DisambiguationError:
			print "Thing"
			continue
		results = wikipedia.search(word)
		if results: 
			summary = wikipedia.summary(word)
			sentences = nltk.sent_tokenize(summary)
			#print summary
			if sentences:
				#print(sentences[0])
				tokens = nltk.word_tokenize(sentences[0])
				tagged = nltk.pos_tag(tokens)
				grammar = "NP: {<V.*><DT>?<JJ>?<NN|NNS>}"
				cp = nltk.RegexpParser(grammar)
				ne_custom = cp.parse(tagged)	
				text = extractEntities(ne_custom)
				print(text)
			#print(page.summary)



stops = stopwords.words('english')
tokens = nltk.word_tokenize(text)

filtered_tokens = [token for token in tokens if token not in punctuation]
filtered_tokens = [token for token in filtered_tokens if token not in stops]
tagged = nltk.pos_tag(filtered_tokens)
 
ne_chunked = nltk.ne_chunk(tagged, binary=False)

def tokenCounts(tokens):
    counts = Counter(tokens)
    sortedCounts = sorted(counts.items(), key=lambda count:count[1], reverse=True)
    return sortedCounts

grammar = "NP: {<DT>?<JJ>*<NN|NNS>}"
cp = nltk.RegexpParser(grammar)
ne_custom = extractEntities(cp.parse(tagged))
print(ne_custom)

wiki=readNltk()
wiki=readEnt()
findWiki(wiki)

print tokenCounts(tagged)





