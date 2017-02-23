import math
from numpy import *

# first get the candidate with TFIDF
open_file = open("TotalCandidateWithTFIDF.pickle","rb")
uiCandidateWithTFIDF = pickle.load(open_file)
open_file.close()
def getUserCandidate(path):
	filename = os.listdir(path)
	usercandidate = []
	for f in filename:
        usercandidate.append(FromFilegetUserInterestCandidate(path,f))
    return usercandidate

def CalucateSum(matrix):
	sum = 0
	for i in range(matrix.shape[0]):
		j = i
		while j < matrix.shape[0]:
			sum += matrix[i][j]
			j += 1
	reutrn sum

def CalucateWeight(usercandidate):
	matrix = []
	for u1 in usercandidate:
		line = []
		for u2 in usercandidate:
			weight = min(usercandidate[u1],usercandidate[u2])
			line.append(weight)
		matrix.append(line)
	matrix = mat(matrix)
	sum = CalucateSum(matrix)
	matrix = matrix * 1.0 / sum
	return matrix

# threshold  
# dampFactor in (0,1)
def CalucateTextRank(ucMatrix,threshold,dampFactor,uid,InitTRMatrix):
	TFIDFMatrix = mat(TotalCandidateWithTFIDF[uid]) * (1 - dampFactor)
	TRMatrix = InitTRMatrix
	oldMatrix = TRMatrix
	# iteration
	iteration = 0
	while True:
		newMatrix = TRMatrix = ucMatrix * TRMatrix.T + TFIDFMatrix
		flag = True
		for i in range(newMatrix.shape[0]):
			for j in range(newMatrix.shape[0]):
				if newMatrix[i][j] - oldMatrix[i][j] > threshold:
					flag = False
					break
		if flag == True:
			break
		iteration += 1
	print "the number of iteration is %d " % iteration
	return TRMatrix


	
