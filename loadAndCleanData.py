# INFO 3401
# Ziyang Zhang, Yizhen Wu, Jason Kibozi-Yocka
# Problem set 3



import pandas as pd
import csv
import numpy as np
# Problem 1
print("This dataset is use for look at the loan risk of investment.")
# Problem 2
def loadAndCleanData(filename):
    item = pd.read_csv(filename)
    item.fillna(value=0,inplace=True)
    print(data)

# Problem 3
newData = loadAndCleanData("creditData.csv")

#Problem 4
import matplotlib.pyplot as plt
def computePDF(columnName, dataSet):
	newPlot = dataSet[columnName].plot.kde()
	plt.show(newPlot)
headers = list(newData.columns.values)
for i in headers:
	computePDF(i, newData)


# Problem 5

#def loadAndCleanData(filename):
#    item = pd.read_csv(filename)
#    data = item.fillna(0)
#    print(data)
#loadAndCleanData("creditData.csv")
def viewDistribution(columnName, dataSet):
	newPlot = dataSet.hist(column = columnName)
	plt.show(newPlot)
columns = list(newData.columns.values)
for i in columns:
	viewDistribution(i,newData)


# Problem 6
def viewLogDistribution(columnName, dataSet):
	newPlot = dataSet.hist(column = columnName, log=True)
	plt.show(newPlot)
logColumns = list(newData.columns.values)
for i in logColumns:
	viewDistribution(i, newData)

# Problem 7
def equalBins(myCol,myDataset):
	myBins = pd.qcut(myDataset[myCol], q=3, duplicates='drop', retbins=False).unique()
	return myBins

# Problem 8
def bintoArray(myNum,myCol,myDataset):
	myBin = (equalBins(myCol,myDataset)[myNum].left,equalBins(myCol,myDataset)[myNum].right)
	return myBin

def computeDefaultRisk(myCol,binLoc,myFeature,myDataset):
	if binLoc == 'right':
		myNum = 0
	if binLoc == 'middle':
		myNum = 1
	if binLoc == 'left':
		myNum = 2
	count = 0
	count2 = 0
	try:
		myBin = bintoArray(myNum,myFeature,myDataset)	
	except:
		return 0.0
	for i, datapoint in myDataset.iterrows():
		if datapoint[myFeature] >= myBin[0] and datapoint[myFeature] < myBin[1]:
			count += 1
			if datapoint[myCol] == 1:
				count2 += 1
	totalSize = len(myDataset)
	prob = count / totalSize
	prob2 = count2 / totalSize
	finProb = prob2 / prob
	return finProb

# Problem 9
myRisks = {}

for feature in newData.columns.values:
	if feature != 'SeriousDlqin2yrs':
		featDict = {}
		featDict['left'] = (computeDefaultRisk('SeriousDlqin2yrs','left',feature,myDataframe)
		featDict['middle'] = computeDefaultRisk('SeriousDlqin2yrs','middle',feature,myDataframe)
		featDict['right'] = computeDefaultRisk('SeriousDlqin2yrs','right',feature,myDataframe)
		myRisks[feature] = featDict

# Problem 10
newLoan=loadAndCleanData("newLoans.csv")

# Problem 11
myWeights = {'age':0.025,'NumberOfDependents':0.025,'MonthlyIncome':0.1,'DebtRatio':0.1,'RevolvingUtilizationOfUnsecuredLines':0.1,'NumberOfOpenCreditLinesAndLoans':0.1,'NumberRealEstateLoansOrLines':0.1,'NumberOfTime30-59DaysPastDueNotWorse':0.15,'NumberOfTime60-89DaysPastDueNotWorse':0.15,'NumberOfTimes90DaysLate':0.15}

myBinDict = {}

for feature in myDataframe.columns:
	if feature != 'SeriousDlqin2yrs':
		mySideDict = {}
		try:
			mySideDict['right'] = equalBins(feature,myDataframe)[0]
		except:
			mySideDict['right'] = None
		try:
			mySideDict['middle'] = equalBins(feature,myDataframe)[1]
		except:
			mySideDict['middle'] = None
		try:
			mySideDict['left'] = equalBins(feature,myDataframe)[2]
		except:
			mySideDict['left'] = None
		myBinDict[feature] = mySideDict

myBinDict

def predictDefaultRisk(myRow,defaults,weights):
	probTable = []
	for feature in myRow.index:
		if feature != 'SeriousDlqin2yrs':
			# check which bin its in
			mybin = ''
			if myRow[feature] in myBinDict[feature]['right']:
				mybin = 'right'
			elif myRow[feature] in myBinDict[feature]['middle']:
				mybin = 'middle'
			elif myRow[feature] in myBinDict[feature]['left']:
				mybin = 'left'
			# get default prob and muliply it by weight
			myNum = defaults[feature][mybin] * weights[feature]
			# add to my probability sum table
			probTable.append(myNum)
	return sum(probTable)
# Problem 12
for row in range(len(myLoanData.index)):
	val = predictDefaultRisk(myLoanData.iloc[[row]],myRisks,myWeights)
	myLoanData['SeriousDlqin2yrs'][row] = val
# Problem 13
computePDF('SeriousDlqin2yrs',testDF)



