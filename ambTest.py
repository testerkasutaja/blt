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


corpus = ['Peeter astus tuppa','Ma jooksin aias']



