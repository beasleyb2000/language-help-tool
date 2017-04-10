# Import libraries
import csv
from os import getcwd

# Define the Dictionary class, which would 
class Dictionary ():
    def __init__(self, srcFile, language):
        self.srcFile = srcFile
        self.addFile = getcwd()+"/addFile.txt"
        self.dictionary = {}
        self.language = language
        
    def makeDict(self):
        self.dictionary = {}
        for row in csv.reader(open(self.srcFile, 'r'), delimiter='|'):
            try:
                self.dictionary[row[0]] = row[1]

            except:
                pass
    
    def order(self):
        srcFileRead = open(self.srcFile, 'r')
        linesToAdd = []
        for line in sorted(srcFileRead):
            linesToAdd.append(line)
        srcFileRead.close()
        srcFileWrite = open(self.srcFile, 'w')
        for line in linesToAdd:
            srcFileWrite.write(line)
        srcFileWrite.close()

    def add(self):
        addFileRead = open(self.addFile, 'r')
        addFileReadCsv = csv.reader(addFileRead, delimiter='|')
        addLines = []
        if self.language == "English":
            for line in addFileReadCsv:
                 addLines.append("{0}|{1}".format(line[0], line[1]))
        else:
            for line in addFileReadCsv:
                if "(verb)" not in line:
                    addLines.append("{0}|{1}".format(line[1], line[0]))
                else:
                     addLines.append("{0}|{1}".format(line[0], line[1]))

        addFileRead.close()

        srcFileAppend = open(self.srcFile, 'a')
        for line in addLines:
            srcFileAppend.write(line+'\n')

        srcFileAppend.close()
        
        self.order()
        
        # Create function to add data to the dicitionaries
    def addToDicts(self, dicts):
        for dictionary in dicts:
            dictionary.add()
    
        addFileClear = open(getcwd()+"/addFile.txt", 'w')
        addFileClear.write("")
        addFileClear.close()

def main():
    # Define file locations
    engFile = getcwd()+"/engFile.txt"
    langFile = getcwd()+"/langFile.txt"
    addFile = getcwd()+"/addFile.txt"
    
    # Create the objects for both of the langauges' dicitonaries
    engDict = Dictionary(engFile, "English")
    langDict = Dictionary(langFile, "Lang")

    # Create the dicitonaries for both the objects, and order them
    engDict.makeDict()
    langDict.makeDict()
    
    engDict.order()
    langDict.order()
    
    # Create an array for the objects to be looped through
    dicts = [engDict, langDict]
    return dicts
