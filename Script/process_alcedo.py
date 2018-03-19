#python3
# NH 2018-01

import re, string, os

def update_filter(text, common_words, proper_nouns):
	"""  """
	place_names=re.findall(r'\n\|([A-ZÁÍÉÓÚÜÑ\-]+)[^\w]', text)
	proper_nouns_new=re.findall(r'[^\.] ([A-ZÁÍÉÓÚÜÑ][a-záéíóúüñ]+)', text) 
	for el in proper_nouns_new:
		if el.lower() not in common_words:
			proper_nouns.update(el)  
	return proper_nouns


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
	return words2check


def text4editor(base, text, checkwords):
	lines=text.split('\n')
	with open('../'+base+'-2check.txt', 'w') as out:
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

	fipath=input('Enter the path of the volume you want to process: ')
	with open(fipath, 'r') as f3:
		text= f3.read()

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
	with open('../Resource/apellidos-es.lst', 'r') as f: # Spanish frequent family names
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
	proper_nouns=set()
	with open('../Resource/alcedo-proper-nouns.lst', 'r') as f: # /!\ This list needs manual supervision /!\ 
		for line in f:
			proper_nouns.update(line.split())
	upd=update_filter(text, common_words, proper_nouns)
	with open('../Resource/alcedo-proper-nouns.lst', 'w') as fo: # update Alcedo's proper nouns list
	    for el in upd:
	        fo.write(el+'\n')
	        filter_words.update(el)
    
	#print(filter_words)
    #	../Corpus/alcedo-vol1-getty-clean.txt
	
	print('Processing text...')
	checkwords=preprocess(text, filter_words)

	print('Tagging noisy tokens...')
	base=os.path.splitext(os.path.basename(fipath))[0]
	text4editor(base, text, checkwords)


	print('Done. Check ../'+base+'-2check.txt')

