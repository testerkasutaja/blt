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
  
def runCaseAnalys(case_dict, list_of_sentences,inappropriateWords):
    go = False
    id_g_es = 0
    id_p = 0
    id_ill = 0
    id_tr_ter_ab_kom = 0
    id_all = 0
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
              (content_all, id_all) = addToContent(word, content_all, casename, id_all, nominative, sen_x,sg_pl)
              if casename == "g" or casename=="es":
                (content_g_es,id_g_es)= addToContent(word, content_g_es, casename, id_g_es, nominative, sen_x,sg_pl)
              if casename == "p":
                (content_p,id_p)= addToContent(word, content_p, casename, id_p, nominative, sen_x,sg_pl)
              if casename == "ill" or casename == "in" or casename == "el" or casename == "adt" or casename == "all" or casename == "ad" or casename == "abl":
                (content_ill,id_ill)= addToContent(word, content_ill, casename, id_ill, nominative, sen_x,sg_pl)
              if casename == "tr" or casename=="ter" or casename=="ab" or casename=="kom":
                (content_tr_ter_ab_kom,id_tr_ter_ab_kom) = addToContent(word, content_tr_ter_ab_kom, casename, id_tr_ter_ab_kom, nominative, sen_x,sg_pl)
              go = False
                
    xmlFormatting(content_g_es)
    xmlFormatting(content_p)
    xmlFormatting(content_ill)
    xmlFormatting(content_tr_ter_ab_kom)
    xmlFormatting(content_all)
    
    tree_g_es.write("laused/omastav_olev.xml",'utf8')
    tree_p.write("laused/osastav.xml","utf8")
    tree_ill.write("laused/kohakäänded.xml","utf8")
    tree_tr_ter_ab_kom.write("laused/saav_rajav_ilma_kaasa.xml","utf8")
    tree_all.write("laused/koik_laused.xml","utf8")

def addToContent(word, content, casename, countid, nominative, sen_x,sg_pl):
              info = SubElement(content,'info')             #XML loomine
              info.set('id', str(countid))
              countid = countid + 1
              s = SubElement(info,'s')
              nr = SubElement(info,'nr')
              case = SubElement(info,'case')
              n = SubElement(info,'n')
              synt = synthesize(nominative, form = sg_pl+' '+casename, phonetic=False)      #kontorll kas leidub rohkem kui üks vastus
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
              return(content,countid)


(combin3,combin4,sentences_with_structure,level2) = getBestPOSCombination(files)
level1_3 = getFinalSentenceListShortSentences(combin3,sentences_with_structure)
level1_4 = getFinalSentenceListShortSentences(combin4,sentences_with_structure)
level1 = level1_3 + level1_4 + level2
runCaseAnalys(case_dict, level1,inappropriateWords)







          
