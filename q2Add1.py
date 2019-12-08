from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import pickle
import os

task = [
'20_newsgroups/rec.sport.baseball',
'20_newsgroups/rec.motorcycles'
]

def fetchFromPickle(pickleFile):
	file = open(pickleFile,'rb')
	pickleData = pickle.load(file)
	file.close()
	return pickleData

def saveInPickle(data, pickleFile):
	file = open(pickleFile,"wb")
	pickle.dump(data,file)
	file.close()

def generateTrigramProb(trigramFreq, bigramFreq, ksmooth,vocSize):

	for w1 in trigramFreq:
		for w2 in trigramFreq[w1]:
			for w3 in trigramFreq[w1][w2]:
				trigramFreq[w1][w2][w3]=float(trigramFreq[w1][w2][w3]+ksmooth)/float(bigramFreq[w1][w2]+ksmooth*vocSize)
	return trigramFreq	

def generateBigramProb(bigramFreq, unigramFreq, ksmooth,vocSize):

	for w1 in bigramFreq:
		for w2 in bigramFreq[w1]:
				bigramFreq[w1][w2]=float(bigramFreq[w1][w2]+ksmooth)/float(unigramFreq[w1]+ksmooth*vocSize)
	return bigramFreq				

def generateUnigramProb(unigramFreq, totalFreq, ksmooth,vocSize):
	for w1 in unigramFreq:
		unigramFreq[w1] = float(unigramFreq[w1]+ksmooth)/float(totalFreq+vocSize*ksmooth)

	return unigramFreq
		
def generateUnigram(data):
	dict = {}
	for word in data:
		dict[word] = 0
	for word in data:
		dict[word]+=1

	return dict	

def generateBigram(data):
	dix = {}
	for i, val in enumerate(data):
		if(i<(len(data)-1)):
			dix[data[i]] = {}
		# print(data[i-1])
		# print(dix)
	# print(dix)	
	for i, val in enumerate(data):
		if(i<(len(data)-1)):
			dix[data[i]][data[i+1]] = 0

	for i, val in enumerate(data):
		if(i<(len(data)-1)):
			dix[data[i]][data[i+1]]+=1	
	# 	dict[data[i]][data[i+1]]+=1
	return dix

def generateTrigram(data):
	dix = {}
	for i, val in enumerate(data):
		dix[data[i]] = {}
		# print(data[i-1])
		# print(dix)
	# print(dix)	
	for i, val in enumerate(data):
		if i < (len(data)-2):
			dix[data[i]][data[i+1]] = {}

	for i, val in enumerate(data):
		if i < (len(data)-2):
			dix[data[i]][data[i+1]][data[i+2]] = 0

	for i, val in enumerate(data):
		if i < (len(data)-2):
			dix[data[i]][data[i+1]][data[i+2]]+=1	
	# 	dict[data[i]][data[i+1]]+=1
	return dix


def removeStopWords(words):
	filteredWords = []
	stop_words=stopwords.words('english')	
	for word in words:
		if word not in stop_words:
			filteredWords.append(word)

	return filteredWords

def processDataSet(path):
	files=[]
	for r, d, f in os.walk(path):
		for file in f:
			files.append(os.path.join(r, file))
	data = []		
	for file in files:
			file = open(file, "r", encoding = "ISO-8859-1")
			fileContent=file.read()
			fileContent=fileContent.lower()
			if (fileContent.find("lines:") != -1):
			 metadata,fileContent = fileContent.split('lines:', 1)
			tokenizer=RegexpTokenizer(r'([A-Za-z0-9]+)')
			dataList=tokenizer.tokenize(fileContent)
			# print(dataList)
			data=data+dataList
			# print(data)
	return data



count = 1
ksmooth = 1
for path in task:
	list = processDataSet(path)
	# list = removeStopWords(list)
	# print(len(list))
	unigramFreq = generateUnigram(list)
	saveInPickle(unigramFreq, "task-"+str(count)+"-unigram-freq.pickle")
	bigramFreq=generateBigram(list)
	saveInPickle(bigramFreq, "task-"+str(count)+"-bigram-freq.pickle")
	trigramFreq=generateTrigram(list)
	saveInPickle(trigramFreq, "task-"+str(count)+"-trigram-freq.pickle")
	totalFreq = len(list)
	vocSize = len(unigramFreq)
	trigramProb = generateTrigramProb(trigramFreq, bigramFreq, ksmooth, vocSize)
	saveInPickle(trigramProb, "add-1-task-"+str(count)+"-trigram.pickle")
	bigramProb = generateBigramProb(bigramFreq, unigramFreq, ksmooth, vocSize)
	saveInPickle(bigramProb, "add-1-task-"+str(count)+"-bigram.pickle")
	unigramProb = generateUnigramProb(unigramFreq, totalFreq, ksmooth, vocSize)
	saveInPickle(unigramProb, "add-1-task-"+str(count)+"-unigram.pickle")
	count+=1
	print(unigramProb)

