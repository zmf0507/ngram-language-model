from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import collections
import pickle
import os
import operator
import math

task = [
'20_newsgroups/rec.sport.baseball', 
'20_newsgroups/rec.motorcycles',
]

def generateUnigramSentence(modelProb, count):
	result=""
	count = int(count)
	# count = 9
	maxProb = 1;
	# sorte = dict( sorted(modelProb.items(), key=operator.itemgetter(0),reverse=True))
	sorte = sorted(modelProb.items(), key=lambda x:x[1], reverse=True)
	# print(sorte[0])
	# print(sorte[1:10])
	# print(socle	rte)
	# sorte = collections.OrderedDict(sorted(modelProb.items()))
	for value in sorte:
		count-=1
		# print(value)
		result += value[0]
		maxProb*=value[1]
		result+=" "
		if(count<=0):
			break
		
	return result, maxProb

def generateBigramSentence(modelProb, count, firstWord):
	firstWord = "i" #the most frequently occuring word in the beginning of a sentence
	result=""
	maxProb=1
	max = 0.000000
	sorte = sorted(modelProb[firstWord].items(), key=lambda x:x[1], reverse=True)
	nextWord = sorte[0][0]
	maxProb*=sorte[0][1]

	result=firstWord+" "+ nextWord
	# print(modelProb[nextWord])
	# maxProb*=max
	# print(maxWord, nextWord)

	for i in range(1, int(count)):
		max = 0.0000000
		sorte  = sorted(modelProb[nextWord].items(), key=lambda x:x[1], reverse=True)

		result+=" "
		nextWord = sorte[0][0]	 
		result+=sorte[0][0]
		maxProb*=sorte[0][1]
		 			
	return result, maxProb	

def generateTrigramSentence(modelProb, count, firstword):
	firstWord = "i"
	result=""
	maxProb=0
	max = 0
	count=int(count)
	# sorte = dict( sorted(modelProb.items(), key=operator.itemgetter(0),reverse=True))
	# for w1 in modelProb:
	# 	for w2 in modelProb[w1]:
	# 		for w3 in modelProb[w1][w2]:
	# 			if(max<modelProb[w1][w2]):
	# 				max = modelProb[w1][w2]
	# 				maxWord = w1
	# 				nextWord = w2

	# 	result=w1+" "+ w2

	for w2 in modelProb[firstWord]:
		sorte  = sorted(modelProb[firstWord][w2].items(), key=lambda x:x[1], reverse=True)
		if(maxProb<sorte[0][1]):
			maxProb = sorte[0][1]
			nextWord = w2
			nextWord2 = sorte[0][0]
	# result=w1+" "+ w2
	result=firstWord +" "+ nextWord + " " + nextWord2
	# print(firstWord,w2, nextWord, maxProb)	

	while(1):
		sorte  = sorted(modelProb[nextWord][nextWord2].items(), key=lambda x:x[1], reverse=True)
		maxProb *= sorte[0][1]
		nextWord = nextWord2
		nextWord2 = sorte[0][0]
		result+= " "+nextWord2
		count-=1
		if(count<1):
			break

	# for i in range(1, count):
	# 	max = 0.0000000
	# 	nextWord = maxWord	
	# 	for w2 in modelProb[nextWord]:
	# 		if(max<modelProb[nextWord][w2]):
	# 			max = modelProb[nextWord][w2]
	# 			maxWord = w2
	# 	result+=" "
	# 	result+=maxWord
	# 	maxProb*=max	  			
	return result, maxProb		

def fetchFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

def saveInPickle(data, pickleFile):
	file = open(pickleFile,"wb")
	pickle.dump(data,file)
	file.close()

def generateSentence(modelProb, ngram, count, firstWord):
	if(ngram=="unigram"):
		return generateUnigramSentence(modelProb, count)
	if(ngram=="bigram"):
		return generateBigramSentence(modelProb, count, firstWord)	
	if(ngram=="trigram"):
		return generateTrigramSentence(modelProb, count, firstWord)	
	


ngrams = ["unigram", "bigram", "trigram"]

# ngrams = ["unigram", "bigram"]
firstWord = ""
print("Enter the length of the sentence")
count = input(int())
for ngram in ngrams:
	print(ngram)
	for task in range(1,3):
		modelProb = fetchFromPickle("task-"+str(task)+"-"+ngram +".pickle")
		# print(modelProb)
		print("TASK-", task)
		result, prob = generateSentence(modelProb, ngram, count, firstWord)
		if(ngram=="unigram"):
			# print(result)
			firstWord = result.split()[0]
		print("Sentence-", result)
		print("maxProbabilty-", math.log(prob,10))
