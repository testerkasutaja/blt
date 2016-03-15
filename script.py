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
case_dict = {'n':'nimetav','sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seestütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")
inappropriateWords = ['surm','suguhaigus','alkohol','seks','perse','tapma','alkoholik','viin']

def formatXMLFile(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      formatXMLFile(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def getPartOfSpeech(list):                            #kontroll, et kõik sõnad oleks üheselt määratud
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

def fixPunctuation(sentence):
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

#KÕIKIDEST FAILIDEST POPULAASREMATE KOMBINATSIOONIDE LEIDMINE
def getBestCombinationsAndSentences(files):          
  combinations3words = {}
  combinations4words = {}
  combinations5words = {}
  structure_with_sentences_3 = {}
  structure_with_sentences_4 = {}
  structure_with_sentences_5 = {}
  for pathStr in files:
    print(pathStr)
    tree = ET.parse(pathStr)
    root = tree.getroot()
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
      sen = elem.text
      sen = fixPunctuation(sen)
      if sen.endswith('.') or sen.endswith('!') or sen.endswith('?'):
        morf_sen = re.sub(',|\.|!|\?|%|"|-|—|”|“', '', sen) # kui lauses on sees: (,),/,\,:,;,* vms märk siis lause ei sobi
        morf_sen = re.sub('  ', ' ', morf_sen)
        morf_sen = re.sub('^ | $', '', morf_sen)
        sen_list = morf_sen.split(' ')
        sen_len = len(sen_list)
        partofspeech = getPartOfSpeech(sen_list)
        if len(partofspeech)>0 and sen_len > 2 and sen_len < 7 and 'Z' not in partofspeech and 'V' in partofspeech:
          partofspeech_str = listtostring(partofspeech)
          if sen_len == 3:
            if partofspeech_str in combinations3words:
              old = combinations3words[partofspeech_str]
              new = old +1
              combinations3words[partofspeech_str] = new
              if sen not in structure_with_sentences_3[partofspeech_str]:
                structure_with_sentences_3[partofspeech_str].append(sen)
            else:
              combinations3words[partofspeech_str] = 1
              structure_with_sentences_3[partofspeech_str] = []
              structure_with_sentences_3[partofspeech_str].append(sen)
          if sen_len == 4:
            if partofspeech_str in combinations4words:
              old = combinations4words[partofspeech_str]
              new = old +1
              combinations4words[partofspeech_str] = new
              if sen not in structure_with_sentences_4[partofspeech_str]:
                structure_with_sentences_4[partofspeech_str].append(sen)
            else:
               combinations4words[partofspeech_str] = 1
               structure_with_sentences_4[partofspeech_str] = []
               structure_with_sentences_4[partofspeech_str].append(sen)
          if sen_len == 5:
            if partofspeech_str in combinations5words:
              old = combinations5words[partofspeech_str]
              new = old +1
              combinations5words[partofspeech_str] = new
              if sen not in structure_with_sentences_5[partofspeech_str]:
                structure_with_sentences_5[partofspeech_str].append(sen)
            else:
               combinations5words[partofspeech_str] = 1
               structure_with_sentences_5[partofspeech_str] = []
               structure_with_sentences_5[partofspeech_str].append(sen)
      #else:
       #print(sen)
  return (combinations3words,combinations4words,combinations5words,structure_with_sentences_3,structure_with_sentences_4,structure_with_sentences_5)

def getCommonSentences(combinations,structure_with_sentences):
  shortSentences= []
  notCommonSen = []
  if len(combinations)>0:
    sorted_com = sorted(combinations.values())
    maximum = sorted_com[-1]
    minimum = (maximum//4)
    print('minimum')
    print(minimum)
    print('maximum')
    print(maximum)
    for k, v in combinations.items():
      if v >= minimum:
        listofsentences = structure_with_sentences.get(k)
        for shortSentences_sentence in listofsentences:
          shortSentences.append(shortSentences_sentence)
      else:
        listofsentences = structure_with_sentences.get(k)
        for shortSentences_sentence in listofsentences:
           notCommonSen.append(shortSentences_sentence)
  print(notCommonSen)
  return(shortSentences)
  
def runCaseAnalys(case_dict, list_of_sentences,inappropriateWords):
  go = False
  id = 0
  content_n = ET.Element('content')
  tree_n = ElementTree(content_n)
  
  content_g_es = ET.Element('content')
  tree_g_es = ElementTree(content_g_es)
    
  content_p = ET.Element('content')
  tree_p = ElementTree(content_p)
    
  content_ill = ET.Element('content')
  tree_ill= ElementTree(content_ill)
    
  content_tr_ter_ab_kom = ET.Element('content')
  tree_tr_ter_ab_kom = ElementTree(content_tr_ter_ab_kom)
    
  content_all=ET.Element('content')
  tree_all = ElementTree(content_all)
    
  if len(list_of_sentences)>0:
    for sentence in list_of_sentences:
      appropriateSentence = True
      sentence = re.sub('^ | $', '', sentence)
      #sentence = re.sub('(^\(|\)$)|(^"|"$)','',sentence)
      morf_sentence = re.sub('(( (,|\.|!|\?|%|#|"))|" |")', '', sentence)
      sentence_list = morf_sentence.split(' ')
      sentence_len = len(sentence_list)
      partofspeech = getPartOfSpeech(sentence_list)              # lause struktuur
      for word in sentence_list:
        if appropriateSentence == True: 
          morf_analyze = analyze(word)
          morf_l2 = morf_analyze[0]['analysis']
          morf_info = morf_l2[0]                              #on ainult 1 (kontrollitakse getBestCombinationsAndSentences(files) funktsioonis)
          case_info =(morf_info['form']).split(' ')
          nominative = morf_info['lemma']
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
              sen_x = re.sub(' '+word+' ',' %%% ',sentence)
              if casename =="n" and sg_pl == "pl":
                (content_all) = addToContent(word, content_all, casename, id, nominative, sen_x,sg_pl)
              if casename != "n":
                (content_all) = addToContent(word, content_all, casename, id, nominative, sen_x,sg_pl)
              if casename == "n" and sg_pl == "pl":
                content_n = addToContent(word, content_n, casename, id, nominative, sen_x, sg_pl)
              if casename == "g" or casename=="es":
                (content_g_es)= addToContent(word, content_g_es, casename, id, nominative, sen_x,sg_pl)
              elif casename == "p":
                (content_p)= addToContent(word, content_p, casename, id, nominative, sen_x,sg_pl)
              elif casename == "ill" or casename == "in" or casename == "el" or casename == "adt" or casename == "all" or casename == "ad" or casename == "abl":
                (content_ill)= addToContent(word, content_ill, casename, id, nominative, sen_x,sg_pl)
              elif casename == "tr" or casename=="ter" or casename=="ab" or casename=="kom":
                  (content_tr_ter_ab_kom) = addToContent(word, content_tr_ter_ab_kom, casename, id, nominative, sen_x,sg_pl)
              id = id + 1
              go = False
          else:
            appropriateSentence = False
                
    formatXMLFile(content_g_es)
    formatXMLFile(content_p)
    formatXMLFile(content_ill)
    formatXMLFile(content_tr_ter_ab_kom)
    formatXMLFile(content_all)
    formatXMLFile(content_n)

    tree_n.write("laused/nimetav.xml",'utf8')
    tree_g_es.write("laused/omastav_olev.xml",'utf8')
    tree_p.write("laused/osastav.xml","utf8")
    tree_ill.write("laused/kohakäänded.xml","utf8")
    tree_tr_ter_ab_kom.write("laused/saav_rajav_ilma_kaasa.xml","utf8")
    tree_all.write("laused/koik_laused.xml","utf8")

def addToContent(word, content, casename, countid, nominative, sen_x,sg_pl):
              info = SubElement(content,'info')             #XML loomine
              info.set('id', str(countid))
              s = SubElement(info,'s')
              nr = SubElement(info,'nr')
              case = SubElement(info,'case')
              n = SubElement(info,'n')
              synt = synthesize(nominative, form = sg_pl+' '+casename, phonetic=False)      #kontorll kas leidub rohkem kui üks vastus
              if len(synt)>1:
                for nom in synt:
                  wordLower = word.lower()
                  nom = re.sub('\?|_', '', nom)
                  #print(" NOM"+nom)
                  if nom == wordLower:
                    answer = SubElement(info, 'word')
                    answer.text = word
                  else:
                    answer = SubElement(info, 'answer')
                    answer.text= nom 
              else:
                answer = SubElement(info, 'word')
                answer.text = word
              n.text = nominative
              nr.text = case_dict[sg_pl]  
              case.text = case_dict[casename]
              s.text = sen_x
              return content


(combin3,combin4,combin5,sentences_with_structure_3, sentences_with_structure_4, sentences_with_structure_5) = getBestCombinationsAndSentences(files)
three_word_sentences = getCommonSentences(combin3,sentences_with_structure_3)
four_word_sentences = getCommonSentences(combin4,sentences_with_structure_4)
five_word_sentences = getCommonSentences(combin5,sentences_with_structure_5)
print('kolm sõna')
print(len(three_word_sentences))
print('neli')
print(len(four_word_sentences))
print('viis')
print(len(five_word_sentences))

all_sentences = three_word_sentences + four_word_sentences + five_word_sentences
runCaseAnalys(case_dict, all_sentences, inappropriateWords)
