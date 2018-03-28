import sys
import math
import io
#reads in the main input file, seperates the first two words, and appends the entire thing into a string
def readLangFile(filename):
    file=io.open(filename, mode='r', encoding='utf8')
    firstly = ""
    for line in file:
        ls=line.split()
        for word in ls:
            firstly += word + " "
    #print(firstly)
    return firstly
    
    #language={}
    #for i in first:
        #if(not(i[0] in language)):
            #language[i[0]]=[i[1]]
        #else:
            #language[i[0]]+=[i[1]]
    #return language            

#cleans the string from the prior function by eliminating the punctionation, large spacing
#and removing all digits.
def cleanText(string):
    new=""
    for i in range(len(string)):
        stuff = string[i]
        if(stuff.isalpha() or stuff == " "):
            new+=stuff.lower()
    return new
            
#makes trigrams out of the input string you include. It iterates through the 
#entire length of whats given and develops a frequency count for it
def makeTrigrams(string):
    trigrams={}
    for i in range(len(string)-2):
        a = string[i]
        b = string[i+1]
        c = string[i+2]
        if(a+b+c in trigrams):
            trigrams[a+b+c]+=1
        else:
            trigrams[a+b+c]=1
    return trigrams

#Fuses one dictionary of trigrams with another dictionary of trigrams, taking 
#what wasn't already in the first dictionary and appending it to it
def fuseDicts(dic1, dic2):
    for trigram in dic2:
        if trigram in dic1:
            dic1[trigram] += dic2[trigram]
        else:
            dic1[trigram] = dic2[trigram]
    return dic1
    
    
#Converts the given integer counts into a percent, scaled out of the total 
#count of the given dictionary 
def convToPercent(dic):
    count = 0
    for key in dic:
        count += dic[key]
    for key in dic:
        dic[key]= dic[key]/count
    return dic

#first main function, opens up a dictionary, then opens and reads the given file
#preforms a for loop identifying the initial contents of the file, then it uses the 
#helper function "readLangFile" which opens up the text embedded file from the original
#input file, cleans it and makes trigrams from it [i.e. "cleansweep"]. After doing so, 
#it begins to check the languages, and brings them into the big dictionary.
def bigDictionary(fileName):
    bigDict={}
    f = open(fileName, 'r')
    for line in f:
        ls=line.split()
        lang=ls[0]
        text=ls[1] 
        cleansweep=makeTrigrams(cleanText(readLangFile(text)))   
        if lang == "Unknown":
            continue
        #here it assigns the original language as the key in the dictionary, and then uses the 
        #helper function "fuseDicts" to take in the current dictionary, and the "cleansweep" variable
        #which made a dictionary of trigrams, and inputs them into the dictionary
        if lang in bigDict:
            bigDict[lang] = fuseDicts(bigDict[lang],cleansweep)
        else:
            bigDict[lang] = cleansweep
    #here it takes the newly inputted dictionary values, of frequency count trigrams, and runs the 
    #helper function "convToPercent" which converts the frequency counts into percentages
    for lang in bigDict:
        bigDict[lang] = convToPercent(bigDict[lang])
    return bigDict

#This is the dictionary, built to identify and store the text files associated with the 
#key indicator known as unknown
def unknownBigDictionary(filename):
    unknown={}
    f=open(filename,'r')
    for line in f:
        ls=line.split()
        lang=ls[0]
        text=ls[1]   
        #if language is equivalent to the unknown, preform the same cleansweeping method
        #and convert the frequency of it into a percentage
        if lang == "Unknown":
            cleansweep=makeTrigrams(cleanText(readLangFile(text)))
            unknown[text] = cleansweep
            unknown[text]=convToPercent(unknown[text])
    return unknown



def pullDict(langdict, unknowns):
    for Uname in unknowns:
        Udict=unknowns[Uname]
        #print(langdict)
        for language in langdict:
            Ldict=langdict[language]
            equate=cosineSimilarity(Udict,Ldict)
            
#here it identifies and runs the initial cosine function of the known and unknown dictionary 
#the input parameters are two main dictionaries that were built.
def cosineSimilarity(known, unknown):
    #alphabet = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o",
    #"p","q","r","s","t","u","v","w","x","y","z"]
    numerator = 0
    A = 0
    B = 0
    #print(unknown)
    for trigram in unknown:
        if trigram in known:
            numerator += known[trigram] * unknown[trigram]
    for trigram in known:
        A += known[trigram]**2
    for trigram in unknown:
        B += unknown[trigram]**2
    equation = numerator / ((A**(1/2)) * (B**(1/2)))
    return equation

#here it compares the cosine similarity between the two dictionaries and starts a new dictionary
#'percentage' where it identifies the name of the file and ensures its in the unknown dictionary keys.
#and then opens a new dictionary and checks that the language is in the known dictionary keys
#if the for loops have been sufficed, then the cosine function similarity is the new value in the sub built dictionary.
#Then the keys of that dictionary, are then later re-inputted as the keys of the 'percentage' dictionaries, which is returned
def compareCosine(known, unknown):
    percentage={}
    for nameOfFile in unknown.keys():
        #{'German' : .89, 'Spanish' : .24}
        howSimilar = {}
        for language in known.keys():
            howSimilar[language] = cosineSimilarity(known[language], unknown[nameOfFile])
            #pullDict(known[language], unknown[nameOfFile])
        percentage[nameOfFile] = howSimilar
    return percentage

#In this function it stores the percentage dictionary that was built. It opens the first arguement, the 'input.txt' file,
#and writes, and runs a for loop for the containments of it. It then re-writes the file name as the indicator, enters a new line, and then list's out a tuple pair of the first element "filename" and the percentage corresponding that filename, with the corresponding original identifying element. Within that list its running a for loop, sorting it by percentage of the file name.

def storePercentage(percentage, filename):
    file=open(filename, 'w')
    #print(percentage)
    for filename in percentage.keys():
        file.write(filename +"\n")
        #print(percentage)
        List=[(k, percentage[filename][k]) for k in sorted(percentage[filename], 
                                    key=percentage[filename].get, reverse=True)]
#This runs a for loop in the list which tabs over the orignial list, identifys the first element, spaces it, and 
#then string writes out the percentage element, and then starts a new line, and ultimately closes the file.
        for toople in List:
            file.write("\t" + toople[0] + " " +str(toople[1]) +"\n")
    file.close()
            

def main():
    input_ = ""
    output_ = ""
    
    if(len(sys.argv) < 2):
        input_ = "input.txt"
        output_ = "output.txt"
    else:
        input_ = sys.argv[1]
        output_ = sys.argv[2]
        
        
    known=bigDictionary(input_)
    #print(known)
    unknown=unknownBigDictionary(input_)
    #print(unknown)
    stuff=compareCosine(known,unknown)
    #print(stuff)
    thing=storePercentage(stuff, output_)
    
    
main()