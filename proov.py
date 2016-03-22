import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import glob
import re
import operator
from pprint import pprint
from estnltk.names import TEXT, ANALYSIS, ROOT, POSTAG, FORM, LEMMA
from estnltk import Disambiguator
from estnltk import synthesize

files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")


def fixPunctuation(sentence):                             #kui lause on " lause lause lasue ? " siis eemaldatakse jutumärgid ( ” , ", “)
  sentence = re.sub('^ | $', '', sentence)
  sentence = re.sub('”$', '', sentence)
  sentence = re.sub('"$', '', sentence)
  if sentence.count('“') == 1 and sentence.count('”')==0:       #“ Mida ise eelistad ? <- et sellistel lausetel  “ märk eemaldada
    sentence = re.sub('“', '', sentence)
  if sentence.count('"') == 1:
    sentence = re.sub('"', '', sentence)
  sentence = re.sub('  ', ' ', sentence)
  sentence = re.sub('^ | $', '', sentence)
  return sentence

def getPosWithMorfaA(corpus):
  posList = []
  disamb = Disambiguator()
  texts = disamb.disambiguate(corpus)
  for text in texts:
    for word in text.words:
        if len(word[ANALYSIS]) > 1:
          #print(word[TEXT],[(a[POSTAG],a[FORM], a[LEMMA]) for a in word[ANALYSIS]])
          return []
        else:
          #print(word[TEXT],[(a[POSTAG],a[FORM], a[LEMMA]) for a in word[ANALYSIS]])
          for a in word[ANALYSIS]:
            partOfSpeech = a[POSTAG]
            if partOfSpeech != 'Z':
              posList.append(partOfSpeech)
  return posList


for pathStr in files:
    print(pathStr)
    tree = ET.parse(pathStr)
    root = tree.getroot()
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}p'):
      corpus = []
      for s in elem:
        sen = s.text
        sen = fixPunctuation(sen)
        if sen.endswith('.') or sen.endswith('!') or sen.endswith('?'):
          corpus.append(sen)  
      posList = getPosWithMorfaA(corpus)
      print(posList)





