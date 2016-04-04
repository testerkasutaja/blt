import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import glob
import re
import operator
from pprint import pprint
from estnltk.names import TEXT, ANALYSIS, ROOT, POSTAG, FORM, LEMMA, CLITIC
from estnltk import Disambiguator
from estnltk import synthesize
from estnltk import Text
from numpy import loadtxt

corpus = [" Ta kaotas tasakaalu raudteejaamadelgi .¤%&"]
synt = synthesize('juht', form = 'sg tr ', hint = 'juhuks')
print(synt)
  
