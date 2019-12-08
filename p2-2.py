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

tasks = [
'20_newsgroups/rec.sport.baseball',
'20_newsgroups/rec.motorcycles',
]

def calculatePerplexity(probability, n):
	perplexity = -(float(probability))/n
	perplexity = pow(10,perplexity)
	return perplexity


def getDataSetSize(unigramFreq):
	dataSetSize = 0
	for word in unigramFreq:
		dataSetSize+=unigramFreq[word]
	return dataSetSize

def setUniOovProbabilty(vocSize, dataSetSize):
	prob = float(1)/float(dataSetSize+vocSize)
	return prob

def setBiOovProbabilty(vocSize, dataSetSize, unigramFreq, wordi_1):
	if(wordi_1 in unigramFreq):
		prob = float(1)/float(unigramFreq[wordi_1]+vocSize)
	else:
		prob = float(1)/float(vocSize) 
	return prob

def setTriOovProbabilty(vocSize, dataSetSize, bigramFreq, wordi_2, wordi_1):
	if(wordi_2 in bigramFreq) and (wordi_1 in bigramFreq[wordi_2]):
		prob = float(1)/float(bigramFreq[wordi_2][wordi_1]+vocSize)
	else:
			prob = float(1)/float(vocSize) 
	return prob

def sentenceProbabiltyUnigram(sentList, trainingData, dataSetSize):
	maxProb = 0
	for word in sentList:
		if(word in trainingData):
			maxProb+=math.log(trainingData[word],10)
		else:
			maxProb+=math.log(setUniOovProbabilty(len(trainingData), dataSetSize), 10)
	return maxProb	

def sentenceProbabiltyBigram(sentList, trainingData, vocsize, dataSetSize, unigramFreq):
	maxProb = 0
	for i, value in enumerate(sentList):
		if(i<len(sentList)-1):
			if(sentList[i] in trainingData) and (sentList[i+1] in trainingData[sentList[i]]):
				maxProb+=math.log(trainingData[sentList[i]][sentList[i+1]],10)
			else:
				maxProb+=math.log(setBiOovProbabilty(vocsize, dataSetSize, unigramFreq, sentList[i]), 10)
	return maxProb	

def sentenceProbabiltyTrigram(sentList, trainingData, vocsize, dataSetSize, unigramFreq, bigramFreq, trigramFreq):
	maxProb = 0
	for i, value in enumerate(sentList):
		if(i<len(sentList)-2):
			if(sentList[i] in trainingData) and (sentList[i+1] in trainingData[sentList[i]]) and (sentList[i+2] in trainingData[sentList[i]][sentList[i+1]]):
				maxProb+=math.log(trainingData[sentList[i]][sentList[i+1]][sentList[i+2]],10)
			else:
				maxProb+=math.log(setTriOovProbabilty(vocsize, dataSetSize, bigramFreq, sentList[i], sentList[i+1]), 10)
	return maxProb	

ngrams = ["unigram", "bigram", "trigram"]

def fetchFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

print("Enter the path of the file")
# path=input()
path = "test.txt"
file = open(path, 'r')
newSent = file.read()
newSent = newSent.lower()
tokenizer=RegexpTokenizer(r'([A-Za-z0-9]+)')
sentList=tokenizer.tokenize(newSent)

trainingData = {}
count = 1
for task in tasks:
	# for ngram in ngrams:
	print("\n",task)
	maxProb=0
	unigramFreq = fetchFromPickle("task-"+str(count)+"-unigram-freq.pickle")
	bigramFreq = fetchFromPickle("task-"+str(count)+"-bigram-freq.pickle")
	trigramFreq = fetchFromPickle("task-"+str(count)+"-trigram-freq.pickle")
	unitraining = fetchFromPickle("add-1-task-"+str(count)+"-unigram.pickle")
	bitraining = fetchFromPickle("add-1-task-"+str(count)+"-bigram.pickle")
	tritraining = fetchFromPickle("add-1-task-"+str(count)+"-trigram.pickle")
	vocabulary = unitraining
	dataSetSize = getDataSetSize(unigramFreq)
	print("UNIGRAM:")
	unigramProbabilty = sentenceProbabiltyUnigram(sentList, unitraining, dataSetSize) 
	print("Probaility:",unigramProbabilty)
	print("Perplexity: ",calculatePerplexity(unigramProbabilty,len(sentList)))
	print("BIGRAM:")
	bigramProbability = sentenceProbabiltyBigram(sentList, bitraining, len(unigramFreq) , dataSetSize, unigramFreq)
	print("Probaility:",bigramProbability)
	print("Perplexity: ",calculatePerplexity(bigramProbability,len(sentList)-1))
	print("TRIGRAM:")
	trigramProbability = sentenceProbabiltyTrigram(sentList, tritraining, len(unigramFreq) , dataSetSize, unigramFreq ,bigramFreq, trigramFreq)
	print("Probaility:", trigramProbability)
	print("Perplexity: ",calculatePerplexity(trigramProbability,len(sentList)-2))
	count+=1
