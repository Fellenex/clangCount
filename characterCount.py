# Author: Chris Keeler, August 22nd 2014

import glob
import math
#
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
		if not(eachFile[len(fileType)*-1:] == fileType[len(fileType)*-1:]):
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

	#print usedFiles
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

def main():
	typedFilesAsString = getAllFileContent(".py", "**")
	sorted = radixSortByDictValue(characterCount(typedFilesAsString))
	for thing in sorted:
		print thing

main()
