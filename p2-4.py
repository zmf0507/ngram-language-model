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

#######GOOD TURING SMOOTHING
#####Assumption, if Nc+1 = 0,Nc+1 = Nc

tasks = [
'20_newsgroups/rec.sport.baseball',
'20_newsgroups/rec.motorcycles',
]

def fetchFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

def setUniOovProbabilty(unigramFreq):
	totalSize = 0
	for word in unigramFreq:
		totalSize+=unigramFreq[word]
	N1 = 0
	for word in unigramFreq:
		if(unigramFreq[word]==1):
			N1+=1
	return (float(N1)/float(totalSize))

def getTrainedUniProbabilty(unigramFreq, word):
	c = unigramFreq[word]
	Nc = 0
	Nc1 = totalSize = 0
	for word in unigramFreq:
		if(unigramFreq[word]==c):
			Nc+=1
		if(unigramFreq[word]==(c+1)):
			Nc1+=1	
		totalSize+=unigramFreq[word]
	# N1 = 0
	# print(Nc1, Nc)
	if(Nc1==0):
		Nc1 = Nc
	prob = float((c+1)*Nc1)/float(Nc*totalSize)
	return prob
		
def getUnigramProbabilty(unigramFreq, sentList):
	maxProb = 0
	for word in sentList:
		if(word in unigramFreq):
			maxProb+=math.log(getTrainedUniProbabilty(unigramFreq, word), 10)
		else:
			maxProb+=math.log(setUniOovProbabilty(unigramFreq), 10)	
	return maxProb

def setBiOovProbabilty(bigramFreq):
	totalSize = 0
	for word in bigramFreq:
		for word2 in bigramFreq[word]:
			totalSize+=bigramFreq[word][word2]
	N1 = 0
	for word in bigramFreq:
		for word2 in bigramFreq[word]:
			if(bigramFreq[word][word2]==1):
				N1+=1
	return (float(N1)/float(totalSize))

def getTrainedBiProbabilty(bigramFreq, word1, word2):
	c = bigramFreq[word1][word2]
	Nc = 0
	Nc1 = totalSize = 0
	for word in bigramFreq:
		for word2 in bigramFreq[word]:
			if(bigramFreq[word][word2]==c):
				Nc+=1
			if(bigramFreq[word][word2]==(c+1)):
				Nc1+=1	
			totalSize+=bigramFreq[word][word2]
	# N1 = 0
	# print(Nc1, Nc)
	if(Nc1==0):
		Nc1 = Nc
	prob = float((c+1)*Nc1)/float(Nc*totalSize)
	return prob
		
def getBigramProbabilty(bigramFreq, sentList):
	maxProb = 0
	for i, val in enumerate(sentList):
		if(i < (len(sentList)-1)):
			if(sentList[i] in bigramFreq) and (sentList[i+1] in bigramFreq[sentList[i]]):
				maxProb+=math.log(getTrainedBiProbabilty(bigramFreq, sentList[i], sentList[i+1]), 10)
			else:
				maxProb+=math.log(setBiOovProbabilty(bigramFreq), 10)	
	return maxProb

def setTriOovProbabilty(trigramFreq):
	totalSize = 0
	for word in trigramFreq:
		for word2 in trigramFreq[word]:
			for word3 in trigramFreq[word][word2]:
				totalSize+=trigramFreq[word][word2][word3]
	N1 = 0
	for word in trigramFreq:
			for word2 in trigramFreq[word]:
				for word3 in trigramFreq[word][word2]:
					if(trigramFreq[word][word2][word3]==1):
						N1+=1
	return (float(N1)/float(totalSize))

def getTrainedTriProbabilty(trigramFreq, word1, word2, word3):
	c = trigramFreq[word1][word2][word3]
	Nc = 0
	Nc1 = totalSize = 0
	for word in trigramFreq:
		for word2 in trigramFreq[word]:
			for word3 in trigramFreq[word][word2]:	
				if(trigramFreq[word][word2][word3]==c):
					Nc+=1
				if(trigramFreq[word][word2][word3]==(c+1)):
					Nc1+=1	
				totalSize+=trigramFreq[word][word2][word3]
	# N1 = 0
	# print(Nc1, Nc)
	if(Nc1==0):
		Nc1 = Nc
	prob = float((c+1)*Nc1)/float(Nc*totalSize)
	return prob
		
def getTrigramProbabilty(trigramFreq, sentList):
	maxProb = 0
	for i, val in enumerate(sentList):
		if(i < (len(sentList)-2)):
			if(sentList[i] in trigramFreq) and (sentList[i+1] in trigramFreq[sentList[i]]) and (sentList[i+2] in trigramFreq[sentList[i]][sentList[i+1]]):
				maxProb+=math.log(getTrainedTriProbabilty(trigramFreq, sentList[i], sentList[i+1], sentList[i+2]), 10)
			else:
				maxProb+=math.log(setTriOovProbabilty(trigramFreq), 10)	
	return maxProb


print("Enter the path of the file")
# path=input()
path="test.txt"
file = open(path, 'r')
newSent = file.read()
newSent = newSent.lower()
tokenizer=RegexpTokenizer(r'([A-Za-z0-9]+)')
sentList=tokenizer.tokenize(newSent)
# sentList = newSent.split()

trainingData = {}
count = 1
for task in tasks:
	# for ngram in ngrams:
	print("\n",task)
	maxProb=0
	unigramFreq = fetchFromPickle("task-"+str(count)+"-unigram-freq.pickle")
	bigramFreq = fetchFromPickle("task-"+str(count)+"-bigram-freq.pickle")
	trigramFreq = fetchFromPickle("task-"+str(count)+"-trigram-freq.pickle")
	# print(unigramFreq['motorcycle'])
	print("unigram:",getUnigramProbabilty(unigramFreq,sentList))
	print("bigram:",getBigramProbabilty(bigramFreq,sentList))
	print("trigram:",getTrigramProbabilty(trigramFreq,sentList))
	count+=1
