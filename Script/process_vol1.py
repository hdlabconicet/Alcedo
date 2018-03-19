#python3
# NH 2018-01

import re, string

def mk_lists(text, common_words):
	""" Extract tokens """
	# noisy tokens
	alphanum=re.findall('([a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]+[0-9]+[a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]*|[a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]*[0-9]+[a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]+)', text)
	# for item in alphanum:
	# 	print(item)

	# named entities
	# place_names=re.findall(r'\n\n\|(\w+)[^\w]', text)
	place_names=re.findall(r'\n\|([A-ZÁÍÉÓÚÜÑ\-]+)[^\w]', text)
	# for item in place_names:
	# 	print(item)

	# ad hoc list
	proper_nouns=re.findall(r'[^\.] ([A-ZÁÍÉÓÚÜÑ][a-záéíóúüñ]+)', text) 
	for el in proper_nouns:
		if el.lower() in common_words:
			proper_nouns.remove(el)
	proper_nouns=set(proper_nouns) # remove duplicates
	# for item in proper_nouns:
	# 	print(item)

	return alphanum, place_names, proper_nouns


def preprocess(text, filter_words):
	""" Text preprocessing """
	# words for manual check 
	words=text.split()
	clean_words=[]
	for word in words:
		word = re.sub(r'([a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]{2,})[,.;?!:\)]', r'\1', word)
		word = re.sub(r'[\|\(]([a-zA-ZáéíóúúñÁÍÉÓÚÜÑ]{2,})', r'\1', word)
		word = re.sub(r'([0-9]{2,})[,.;?!:\)]', r'\1', word)
		clean_words.append(word)
	uniq_words=set(clean_words)
	words2check=uniq_words.difference(filter_words)
	#print(len(words2check)) 

	# ad hoc list
	#for word in words2check:
	# 	if word.islower() and len(word)>3 and not word.isdigit():
	# 		print(word)
		#if len(word)>3 and not word.isdigit()
			#print(word)
	
	return words2check


def text4editor(text, checkwords):
	lines=text.split('\n')
	with open('../alcedo-vol1-getty-2check.txt', 'w') as out:
		for line in lines:
			words=line.split()
			for item in checkwords:
				if item in words:
					if item in [',','.',';']:
						pass
					else:
						line=line.replace(item, '___'+item+'___')
			out.write(line+'\n')
	

if __name__ == '__main__':
	print('Building filter...')
	filter_words= set()
	common_words=set()

	with open('../Resource/freq-words-pelagios-ext.lst', 'r') as f: # vocabulary from similar texts
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/stopwords-spa-nltk.lst', 'r') as f: # Spanish stopwords from NLTK
		for line in f:
			filter_words.update(line.split())
			common_words.update(line.split())
	with open('../Resource/stoplist-spa.lst', 'r') as f: # more Spanish stopwords 
		for line in f:
			filter_words.update(line.split())
			common_words.update(line.split())
	with open('../Resource/80k-words-spa.lst', 'r') as f: # Spanish frequent words
		for line in f:
			filter_words.update(line.split())
			common_words.update(line.split())
	with open('../Resource/apellidos-es.lst', 'r') as f: # Spanish frequent familiy names
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/nombres-propios-es.lst', 'r') as f: # Spanish frequent names
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/10k-words-spa-rae.lst', 'r') as f: # Spanish frequent words RAE
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/roman-numbers.lst', 'r') as f: # for centuries and chapter numbers
		for line in f:
			filter_words.update(line.split())
	# ad hoc lists
	with open('../Resource/alcedo-numbers.lst', 'r') as f: 
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/alcedo-words.lst', 'r') as f: 
		for line in f:
			filter_words.update(line.split())
	with open('../Resource/alcedo-proper-nouns.lst.sort', 'r') as f: # /!\ This list needs manual supervision /!\ 
		for line in f:
			filter_words.update(line.split())

	#print(filter_words)

	print('Processing text...')
	with open('../Corpus/alcedo-vol1-getty-clean.txt', 'r') as f3:
		v1_getty= f3.read()
	
	#print(mk_lists(v1_getty, common_words))
	
	checkwords=preprocess(v1_getty, filter_words)

	print('Tagging noisy tokens...')
	text4editor(v1_getty, checkwords)
	#text4editor('|COQUIBACOA, Cabo de) Punta\n\n de L)^CO¿l tierra, que \in sale al  á i)® : mar en la Coeta de la Provincia y ', checkwords)

	print('Done. Check \'../alcedo-vol1-getty-2check.txt\'')


	# with open('../Corpus/alcedo-vol1-duke-clean.txt', 'r') as f2:
	# 	v1_duke= f2.read()
	#print(preprocess(v1_duke, filter_words))
