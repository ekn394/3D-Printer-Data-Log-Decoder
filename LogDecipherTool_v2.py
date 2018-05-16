# Cubicon Log File Decoder
# Evan Nordquist
# May 14, 2018
# Version 1. Brainstorming
# Version 2. Searches for .txt files in the same directory to build the list of log files to decipher. 

'''
Make a program that can:
1.  Open the .txt log files
2.  Divide the text into sections of individual print jobs (start and end times)
3.  Isolate the portion of text for the time stamps
4.  Convert text "time stamps" into time formatted NUMBERS, instead of TEXT. 
5.  Calculate the print time for each print job.
6.  Add the time for each print job to a running total for that log file


Stretch goals

7.  Have the program keep track of which log files have already been read
8.  Manage an overall "Total printing time" per printer.
9.  Output the data into a more useful format than the txt files we have now.
'''



#################################
# Modules and  Global Variables #
#################################
import glob

log_file_original = ""
log_file_working = ""
timeStampList = []
tempTimeStampList = []
printJobTitle = ""
printJobTitleList = []
runningPrintJobTitleList = []
printTimeSecList = []
dailyPrintTimeSecList = []
runningPrintTimeSec = 0
dailyPrintTimeSec = 0
logName = ""
num_lines = 0
num_print_jobs = 0


files = (glob.glob("*.txt"))

####################
# Helper Functions #
####################

def openLogFile(textFileName):
    #Opens the .txt log file and creates a python objects (original and working) of the text file's contents.
    #The textfile is in the same directory as this python script.
    global log_file_working, log_file_original, logName
    txt = open(textFileName)
    logName = textFileName
    log_file_working = txt.read()
    log_file_original = txt.read()


def findCurrentPrintJobTitle(someString):
    #The name of the print job is found after the third ":" and before the final ".hfb"
    global printJobTitle
    global printJobTitleList, runningPrintJobTitleList
    first_colon = someString.find(":")
    second_colon = someString.find(":", first_colon + 1)
    third_colon = someString.find(":", second_colon + 1)
    first_hfb = someString.find(".hfb", third_colon + 1)
    printJobTitle = someString[third_colon+2:first_hfb]
    printJobTitleList.append(printJobTitle)
    runningPrintJobTitleList.append(printJobTitle)
    return printJobTitle


def findPrintJobTimeStamp(someString):
    global timeStampList
    global tempTimeStampList
    #Given that the timestamp ends 
    first_colon = someString.find(":")
    second_colon = someString.find(":", first_colon + 1)
    timeStampEnd = someString.find(" ", second_colon)
    #print ("My prediction is that the time for this line was")
    timeStamp = someString[:timeStampEnd]
    timeStampList.append(timeStamp)
    tempTimeStampList.append(timeStamp)
    return timeStamp


def eraseLine(someString):
    global log_file_working
    first_colon = someString.find(":")
    second_colon = someString.find(":", first_colon + 1)
    third_colon = someString.find(":", second_colon + 1)
    first_hfb = someString.find(".hfb", third_colon + 1)
    end_of_the_line = first_hfb + 5
    someString = someString[end_of_the_line:]
    log_file_working = someString
    #print log_file_working
    

def determinePrintJobTime():
    global timeStampList
    global tempTimeStampList
    global runningPrintTimeSec, printTimeSecList, dailyPrintTimeSec, dailyPrintTimeSecList
    #print tempTimeStampList
    start = tempTimeStampList.pop(0)
    end = tempTimeStampList.pop(0)
    timeformatted = start[:2] + start[3:5] + start[6:8]
    startInSeconds = ((int(start[:2])) * 3600 ) + ((int(start[3:5])) * 60) + int(start[6:8])
    endInSeconds = ((int(end[:2])) * 3600 ) + ((int(end[3:5])) * 60) + int(end[6:8])
    difference = endInSeconds - startInSeconds
    printTimeSecList.append(difference)
    dailyPrintTimeSecList.append(difference)
    dailyPrintTimeSec = dailyPrintTimeSec + difference
    runningPrintTimeSec = runningPrintTimeSec + difference



def decodeNextPrintJob():
    findCurrentPrintJobTitle(log_file_working)
    findPrintJobTimeStamp(log_file_working)
    eraseLine(log_file_working)
    findPrintJobTimeStamp(log_file_working)
    determinePrintJobTime()
    eraseLine(log_file_working)


def decodeBulkSeconds(seconds):
	hours = seconds//3600
	if hours < 10:
		hours = str("0"+str(hours))
	mins = ((seconds%3600)//60)
	if mins < 10:
		mins = str("0"+str(mins))	
	secs = ((seconds%3600)%60)
	if secs < 10:
		secs = str("0"+str(secs))
	return (str(hours)+":"+ str(mins)+":" + str(secs))


def dailySummaryReport():
    items = len(dailyPrintTimeSecList)
    loopCounter = 0
    print ("***********************************")
    print ("Summary Report " + logName)
    print ("***********************************")
    while loopCounter < items :
        print (str(decodeBulkSeconds(dailyPrintTimeSecList[loopCounter])) + "\t" + str(printJobTitleList[loopCounter]) + " ")  
        loopCounter = loopCounter + 1
    print ("___________________________________")

    print ("Daily Totals")

    print (str(items) + " print jobs total.")
    print (str(decodeBulkSeconds(dailyPrintTimeSec)) + " daily print time.")

    print ("")
    print ("")
    print ("")

def linesPerTextFile(fileName):
	global num_lines
	num_lines = sum(1 for line in open(fileName))
	return num_lines


def decodeAllLines(fileName):
	global num_lines, num_print_jobs
	linesPerTextFile(fileName)
	num_print_jobs = int(linesPerTextFile(fileName)/2.0)
	i = 0
	while i < num_print_jobs:
		decodeNextPrintJob()
		i = i + 1

####################
# Main  Game Logic #
####################

def main():
	global files, dailyPrintTimeSec, dailyPrintTimeSecList, printJobTitleList
	for logFile in files:
		openLogFile(logFile)
		decodeAllLines(logFile)
		dailySummaryReport()
		dailyPrintTimeSec = 0
		dailyPrintTimeSecList = []
		printJobTitleList = []
	print ("***********************************")
	print ("Overall")
	print ("***********************************")
	print (str(decodeBulkSeconds(runningPrintTimeSec)) + " total printing time found on this USB.")
	print ("There were " + str(len(runningPrintJobTitleList)) + " print jobs found over " + str(len(files)) + " days of log files.")
	print ("")
	print ("")
	print ("")

###################
# Run the Program #
###################

main()

