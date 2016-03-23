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
from estnltk import Text
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")


sentence=' " Vajad sa lampi ? " '
def fixPunctuation(sentence):                             #kui lause on " lause lause lasue ? " siis eemaldatakse jutumärgid ( ” , ", “)
  sentence = re.sub('^\s|\s$', '', sentence)
  sentence = re.sub('”', '"', sentence)
  sentence = re.sub('“', '"', sentence)
  if sentence.count('"')== 4 and sentence.endswith('"') and sentence.startswith('"') :      #Sobivad laused "Tere," ütles Peeter "kuidas läheb?".
    return sentence
  if sentence.count('"')== 1 or sentence.count('"')== 3 or sentence.count('"') > 4 :
    sentence = ""
    return sentence
  if sentence.count('"')== 2 and sentence.endswith('"') and sentence.startswith('"'):
    sentence = re.sub('^"|"$', '', sentence)
  
  sentence = re.sub('\s\s', ' ', sentence)
  sentence = re.sub('^\s|\s$', '', sentence)
  return sentence




print(fixPunctuation(sentence))
