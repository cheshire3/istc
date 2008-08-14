#!/home/cheshire/cheshire3/install/bin/python 
# -*- coding: utf-8 -*-

import time, sys, os
osp = sys.path
sys.path = ["/home/cheshire/cheshire3/cheshire3/code"]
sys.path.extend(osp)
from www_utils import *
import os, re

#a = re.compile('<.*?>(.*?)</.*?>') # istc No
#logfile = open("logquote.txt", 'w')

repDict = {'' : '',
           '' : '',
           "'" : " &#39;",
           'à' : '&#96;',
           'á' : ' &#225;',
           '&abreve;' : '&#259;',
           'ć' : '&#263;',
           'ę' : '&#280;',
           'é' :  '&#233;',
           'è' : '&#232;',
           '&egrave;' : '&#232;',
           '&ebreve;' : '&#277;',
           '&îcirc;' : '&#110;',
           '&îgrave;' : '&#236;',
           '&îacute;' : '&#237;',
           '&îbreve;' : '&#301;',
           '&iszlig;' : '&#95;',
           'Ã®' : '&#110;',
           'ł' : '&#322;',
           '&lstrok;' : '&#322;',
           'ń' : '&#324;',
           '&nbreve;' : '&#328;',
           '&oslash;' : '&#120;',
           '&obreve;' : '&#365;',
           'Ö' : '&#86;',
           'ó' : '&#243;',
           'ö' : '&#246;',
           'Š' : '&#352;',
           '&tcaron;' : '&#357;',
           'ü' : '&#252;',
           '&ubreve;' : '&#365;',
           '&uuml;' : '&#124;',
           '&zacute;' : '&#378;',
           '&zdot;' : '&#380;',
           'K&bslash;enhavn' : 'K&oslash;benhavn',
           'K&Bslash;enhavn' : 'K&oslash;benhavn',
           'colec&tbreve;iei' : 'colec&#355;iei',
           'Saj�-Solt�sz' : 'Saj&#83;-Solt&#105;sz',
           'G�nt' : 'G&#124;nt',
           'Gen�ve' : 'Gen&#104;ve'
           }

listFiles = os.listdir("oldformdata/")

for file in listFiles:
    #print file
    dataFile = open("oldformdata" +"/" + file, 'r')
    dataString = dataFile.read()
    dataString = multiReplace(dataString, repDict)
    dataString = dataString.replace('&amp;#', '&#')

        
    dataWrite = open("datatest/" + file, 'w')
    dataWrite.write(dataString)
    dataWrite.close
    dataFile.close
