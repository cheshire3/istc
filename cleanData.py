#!/usr/bin/python
#!/home/cheshire/install/bin/python 

import os, re

#a = re.compile('<.*?>(.*?)</.*?>') # istc No
#logfile = open("logquote.txt", 'w')
listFiles = os.listdir("data/")

for file in listFiles:
    #print file
    dataFile = open("data" +"/" + file, 'r')
    dataString = dataFile.read()
    dataString = dataString.replace('ü', '&#252;').replace('ó', '&#243;').replace('ö', '&#246;').replace('á', ' &#225;').replace('é',  '&#233;').replace("'", " &#39;").replace('è', '&#232;').replace('&amp;#', '&#')
    
        
    dataWrite = open("data2/" + file, 'w')
    dataWrite.write(dataString)
    dataWrite.close
    dataFile.close
