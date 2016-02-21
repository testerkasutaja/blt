import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import glob
import re
import operator
from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint


#käänete sõnastik
case_dict = {'sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seesütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")
inappropriateWords = ['surm','suguhaigus','alkohol']

def xmlFormatting(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      xmlFormatting(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i  
  

def getPartOfSpeech(list):                                   #kontroll, et kõik sõnad oleks üheselt määratud
  partofspeech = []
  for word in list:
    morf_l = analyze(word)
    if len(morf_l)>0:
      morf_l2 = morf_l[0]['analysis']
      if len(morf_l2) != 1:                           #üheselt määratavuse kontroll
        return []
      else:
        b = morf_l2[0]
        pos = b['partofspeech']
        partofspeech.append(pos)
  return partofspeech


def listtostring(list):
  str = ', '.join(list)
  return str


#KÕIKIDEST FAILIDEST POPULAASREMATE KOMBINATSIOONIDE LEIDMINE esimese leveli jaoks (neljasõnalised laused)
def getBestPOSCombination(files):          
  combinations3words = {}
  combinations4words = {}
  structure_with_sentences_short = {}
  sentences_long = []
  for pathStr in files:
    print(pathStr)
    tree = ET.parse(pathStr)
    root = tree.getroot()
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
        sen = elem.text
        sen = re.sub('^ | $', '', sen)
        morf_sen = re.sub('(( (,|\.|!|\?|%|#|"))|" )', '', sen)
        sen_list = morf_sen.split(' ')
        sen_len = len(sen_list)
        partofspeech = getPartOfSpeech(sen_list)
        if len(partofspeech)>0 and sen_len > 2 and sen_len < 5 and 'Z' not in partofspeech and 'V' in partofspeech:
          partofspeech_str = listtostring(partofspeech)      
          if partofspeech_str in combinations3words or partofspeech_str in combinations4words :
            if sen_len == 3:
              old = combinations3words[partofspeech_str]
              new = old +1
              combinations3words[partofspeech_str] = new
            else:
              old = combinations4words[partofspeech_str]
              new = old +1
              combinations4words[partofspeech_str] = new
            structure_with_sentences_short[partofspeech_str].append(sen)
          else:
            if sen_len==3:
              combinations3words[partofspeech_str] = 1
            else:
              combinations4words[partofspeech_str] = 1
            structure_with_sentences_short[partofspeech_str] = []
            structure_with_sentences_short[partofspeech_str].append(sen)

        elif partofspeech != [] and sen_len > 4 and sen_len > 10 and 'V' in partofspeech and 'S' in partofspeech:
           sentences_long.append(sen)
  #print(structure_with_sentences_4word)
  #print(sentences_morethan4word)
  return (combinations3words,combinations4words,structure_with_sentences_short,sentences_long)


def getFinalSentenceListShortSentences(combinations,structure_with_sentences_short):
  level1= []
  if len(combinations)>0:
    sorted_com = sorted(combinations.values())
    maximum = sorted_com[-1]
    minimum = (maximum//1.5)
    #print(minimum)
    #print(combinations)
    for k, v in combinations.items():
      if v >= minimum:
        listofsentences = structure_with_sentences_short.get(k)
        for level1_sentence in listofsentences:
          level1.append(level1_sentence)
  return(level1)
  
def runCaseAnalys(case_dict, list_of_sentences, file_name,inappropriateWords):
    go = False
    countid=0
    content = ET.Element('content')
    tree2 = ElementTree(content)
    if len(list_of_sentences)>0:
      for sen in list_of_sentences:
        sen = re.sub('^ | $', '', sen)
        morf_sen = re.sub('(( (,|\.|!|\?|%|#|"))|" )', '', sen)
        sen_list = morf_sen.split(' ')
        sen_len = len(sen_list)
        partofspeech = getPartOfSpeech(sen_list)              # lause struktuur
        for word in sen_list:
          morf_l = analyze(word)
          morf_l2 = morf_l[0]['analysis']
          b = morf_l2[0]
          case_info =(b['form']).split(' ')
          if len(b['root_tokens']) == 1:
            nominative = b['root_tokens'][0]
          elif len(b['root_tokens']) == 2:
            nominative = b['root_tokens'][0]+b['root_tokens'][1]
          else:
            #print(b['root_tokens'])
            nominative = b['root_tokens'][0]+b['root_tokens'][1]+b['root_tokens'][2]
          if nominative not in inappropriateWords:
            if case_info[0]=='adt':                           #Lühikesisseütlev
              casename = case_info[0]
              sg_pl='sg'
              go = True
            elif len(case_info)== 2 and case_info[0] in case_dict and case_info[1] in case_dict: #kui on käändsõna
              sg_pl = case_info[0]                            # ainus v mitmus   
              casename = case_info[1]                         # kääne
              go = True
            if go == True:                
              sen_x = re.sub(word,'%%%',sen)
              info = SubElement(content,'info')              #XML loomine
              info.set('id', str(countid))
              countid = countid + 1
              s = SubElement(info,'s')
              nr = SubElement(info,'nr')
              case = SubElement(info,'case')
              n = SubElement(info,'n')
              synt = synthesize(nominative, form = sg_pl+' '+casename, phonetic=False)      #kontorll kas leidub rohkem kui üks vastus
              #if sg_pl == "pl":                                    Nimeta vormi mitmuse saamine
                #plurar_nominative = synthesize(nominative, form = 'pl n', phonetic=False)
                #nominative=plurar_nominative[0]
                #nominative = nominative.replace("_", "")
              if len(synt)>1:
                for nom in synt:
                  nom = re.sub('_','',nom)
                  answer = SubElement(info, 'answer')
                  answer.text= nom 
              else:
                answer = SubElement(info, 'answer')
                answer.text = word
              n.text = nominative
              nr.text = case_dict[sg_pl]  
              case.text = case_dict[casename]
              s.text = sen_x
              go = False
                      
    xmlFormatting(content)
    tree2.write(file_name,'utf8')




(combin3,combin4,sentences_with_structure,level2) = getBestPOSCombination(files)
level1_3 = getFinalSentenceListShortSentences(combin3,sentences_with_structure)
level1_4 = getFinalSentenceListShortSentences(combin4,sentences_with_structure)
level1 = level1_3 + level1_4 + level2
runCaseAnalys(case_dict, level1, 'laused.xml' ,inappropriateWords)







          
