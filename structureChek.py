import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import glob
import re
import operator
from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")

for pathStr in files:
    print(pathStr)
    tree = ET.parse(pathStr)
    root = tree.getroot()
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
        sen = elem.text
        sen = re.sub('^ | $', '', sen)
        sen = re.sub('”$', '', sen)
        sen = re.sub('"$', '', sen)
        if sen.count('“') == 1 and sen.count('”')==0:       #“ Mida ise eelistad ? <- et sellistel lausetel  “ märk eemaldada
            sen = re.sub('“', '', sen)
        if sen.count('"') == 1:
            sen = re.sub('"', '', sen)
        morf_sen = re.sub('(( (,|\.|!|\?|%|#|"|\)|\(|-))|" |"|“|“ |\.)', '', sen)
        morf_sen = re.sub('^ | $', '', morf_sen)
        #print(morf_sen)
        sen_list = morf_sen.split(' ')
        sen_len = len(sen_list)
        if sen_len > 2 and sen_len < 6:
            if sen.count('(')==1:
                print (sen)
        
        #if len(partofspeech)>0 and sen_len > 2 and sen_len < 6 and 'Z' not in partofspeech and 'V' in partofspeech:


# !!!! tuleb sisse panna et if sen.count('"')>=3: siis ei sobi lause
