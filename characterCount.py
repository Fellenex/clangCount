# Author: Chris Keeler, August 22nd 2014

import glob
import math
import matplotlib.pyplot as plt
import numpy as np

#This function checks to see if a file has a specific extension
def hasExtension(fileName, extension):
	return (fileName[len(extension)*-1:] == extension)


# This function collects the text of all of the files in this directory and
# every subdirectory
#
# Parameters:
#	directory: a string to be used as the search directory
#
# Return Value:
#	countDict: a dictionary where the keys are the unique characters, and
#				the values are the number of occurrences of that character.
#
def getAllFileContent(fileType, searchDirectory):
	print glob.glob(searchDirectory)

	content = ""
	usedFiles = []
	for eachFile in glob.glob(searchDirectory):
		
		if not(hasExtension(eachFile, fileType)):
			#print "different "+eachFile[len(fileType)*-1:]+"||||"+fileType[len(fileType)*-1:]
			continue
		else:
			#print "Found one! "+eachFile[len(fileType)*-1:]
			try:
				fileObject = open(eachFile, 'r');
				usedFiles.append(eachFile)
				
				for line in fileObject:
					content+=(line.rstrip('\r\n'))
				
				fileObject.close()
				
			except IOError:
				print "Couldn't open "+eachFile
	return content

#
# This function takes a string and returns a dictionary where the keys are the characters, and
# the values are the number of times that the character occurs in  the string
#
# Parameters:
#	searchMe: a string to be examined for character counts
#
# Return Value:
#	countDict: a dictionary where the keys are the unique characters, and
#				the values are the number of occurrences of that character.
#
def characterCount(searchMe):
	countDict = dict()
	for i in range(len(searchMe)):

		if searchMe[i] in countDict:
			countDict[searchMe[i]] += 1
		else:
			countDict[searchMe[i]] = 1

	return countDict

#How does this work?
#I am not sure.
def radixSortByDictValue(dictToSort):
	#dict.items() returns a list like [(key1, val1), (key2, val2), ...]
	dictCouples = list(dictToSort.items())
	size = len(dictCouples)
	phaseOneBins = []
	phaseTwoBins = []
	for i in range(size):
		phaseOneBins.append([])
	
	for i in range(size*size):
		phaseTwoBins.append([])
	
	for charAndCount in dictCouples:
		#The character is the 0 index and the count is the 1 index
		index = charAndCount[1] % size
		phaseOneBins[index].append(charAndCount)
	
	flattenedList = []
	for bin in phaseOneBins:
		for charAndCount in bin:
			flattenedList.append(charAndCount)
	
	for charAndCount in flattenedList:
		index = int(math.floor(charAndCount[1]))
		phaseTwoBins[index].append(charAndCount)
	
	finalList = []
	for bin in phaseTwoBins:
		for charAndCount in bin:
			finalList.append(charAndCount)
	
	return finalList


#
# This function creates a bar graph, where the x axis is lined with different character bins,
# and the y axis is lined with character frequency values
#
# Parameters:
#	charFrequencyTuples: A list of tuples of the form (x,y), where x is a character, and y is the frequency of that character
#	fileName: A file name to be used for the saved .png
#
# Return Value:
#	None
def barGraph(charFrequencyTuples, fileName):
	#unzip the list of tuples into two lists.
	charBins = []
	frequencies = []
	for eachTup in charFrequencyTuples:
		charBins.append(eachTup[0])
		frequencies.append(eachTup[1])
	
	fig = plt.figure()	
	
	#1x1 grid, first subplot
	ax = fig.add_subplot(111)

	#The number of bins
	N = len(frequencies)
	
	#necessary variables
	ind = np.arange(0,N,1)                # the x locations for the groups
	width = 0.8                      # the width of the bars

	tickRange = np.arange(0,1,1)
	
	# the bars
	rects1 = ax.bar(ind, frequencies, width, color='black')
	
	# axes and labels
	#ax.set_xlim(-width,len(ind)+width)
	ax.set_ylim(0,frequencies[-1]*1.1) #Set the y max at 110% of the maximum frequency value
	ax.set_ylabel('Frequency')
	ax.set_xlabel('Characters')
	ax.set_title('Characters by Frequency')
	
	#This line sets a serious amount of space between each bin.
	#ax.set_xticks(ind, charBins)
	
	
	ax.set_xticks(ind+width)
	
	xTickNames = ax.set_xticklabels(charBins, ha='left')

	#Formats the bins
	plt.setp(xTickNames, rotation=0, fontsize=10)

	plt.show()

	plt.savefig(fileName+'.png')

#
# This function saves a CSV representing the character frequency for a set of evaluated files.
#
# Parameters:
#	charFrequencyTuples: A list of tuples of the form (x,y), where x is a character, and y is the frequency of that character
#	fileName: A file name to be used for the saved .txt
# 
# Return Value:
#	None
def saveFrequencyCSV(charFrequencyTuples, fileName):
	with open(fileName+'.txt', 'w') as csvObj:
		csvObj.write("bin,frequency\n")
		i=0
		while i<len(charFrequencyTuples):
			csvObj.write(str(charFrequencyTuples[i][0])+','+str(charFrequencyTuples[i][1])+'\n')
			i+=1
	
	#Make sure everything is cleaned up
	if not(csvObj.closed):
		csvObj.close

def main():
	typedFilesAsString = getAllFileContent(".py", "**")
	sorted = radixSortByDictValue(characterCount(typedFilesAsString))
	for thing in sorted:
		print thing
	barGraph(sorted, "myPy")
	#saveFrequencyCSV(sorted,"myPy")

main()
