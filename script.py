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
inappropriateWords = ['']
def xml_formatting(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      xml_formatting(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i  
  
def structureCompatibilityLevel1(list):
  structure = {'P':{'S':{'V':{'S':True}},'D':{'A':{'S':True}}},'S':{'S':{'D':{'S':True}}},'H':{'V':{'S':{'S':True}}}}
  if 'V' in list:
    if len(list)==3 :
      a,b,c = list[0],list[1],list[2]
      try:
        structure[a][b][c]
        return True
      except KeyError:
        return False
    if len(list)==4 :
      a,b,c,d = list[0],list[1],list[2],list[3]
      try:
        structure[a][b][c][d]
        return True 
      except KeyError:
        return False

def structureCompatibilityLevel2(list):
  if 'V' in list and 'S' in list:
    return True

#P = ['V','S','D','S']  

#print(structureCompatibilityLevel1(P))

def getPartOfSpeech(list):                                   #kontroll, et kõik sõnad oleks üheselt määratud
  partofspeech = []
  for word in list:
    morf_l = analyze(word)
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
#print(listtostring(['a','b','c']))

#KÕIKIDEST FAILIDEST POPULAASREMATE KOMBINATSIOONIDE LEIDMINE esimese leveli jaoks (neljasõnalised laused
def getBestPOSCombination(case_dict, files):          
  combinations = {}
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
        if partofspeech != [] and sen_len > 3 and sen_len <5 and 'Z' not in partofspeech and 'V' in partofspeech and ('S' in partofspeech or 'A' in partofspeech or 'U' in partofspeech  or 'C' in partofspeech or 'N' in partofspeech or 'O' in partofspeech or 'p' in partofspeech):
          partofspeech_str = listtostring(partofspeech)      
          if partofspeech_str in combinations:
            old = combinations[partofspeech_str]
            new = old +1
            combinations[partofspeech_str] = new
            #print(partofspeech_str)
          else:
            combinations[partofspeech_str] = 1
            #print(partofspeech_str)
  sorted_com = sorted(combinations.values())
  maximum = sorted_com[-1]
  print(maximum)
  return combinations

comb = {'S, V, P, A': 3, 'S, V, S, V': 2, 'D, V, D, S': 2, 'J, D, V, S': 1, 'S, G, V, D': 1, 'S, V, P, V': 3, 'P, V, P, S': 2, 'J, S, V, V': 2, 'D, V, S, S': 1, 'V, J, V, S': 3, 'D, V, P, S': 2, 'J, P, V, S': 2, 'V, V, D, S': 1, 'P, V, A, S': 5}

def combintolist(combinations):
  structure = {}
  sorted_com = sorted(combinations.values())
  maximum = sorted_com[-1]
  minimum = 2
  for k, v in combinations.items():
    if v <= maximum and v >= minimum:
      key_list = k.split(', ')
      print(key_list)
      p = {}
      p2 = {}
      for i in  range(len(key_list)-1,-1,-1):
        print(i)
        if i == len(key_list)-1:
          p[key_list[i]] = True   
        else:
          p2[key_list[i]] = p
          p=p2
          p2 = {}
      print(p)

  
combintolist(comb)
  
def runCaseAnalys(case_dict, pathStr, file_name):
    go = False
    tree = ET.parse(pathStr)
    root = tree.getroot()
    countid=0
    content = ET.Element('content')
    tree2 = ElementTree(content)
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
        sen = elem.text
        sen = re.sub('^ | $', '', sen)
        morf_sen = re.sub('(( (,|\.|!|\?|%|#|"))|" )', '', sen)
        sen_list = morf_sen.split(' ')
        sen_len = len(sen_list)
        partofspeech = getPartOfSpeech(sen_list)              # lause struktuur
        compatibility1 = structureCompatibilityLevel1(partofspeech)
        compatibility2 = structureCompatibilityLevel2(partofspeech)
        if sen_len > 3 and sen_len <5 and len(partofspeech) > 0: # and (compatibility1 == True or compatibility2 == True):                           #Lause on 3-4 sõna ja on unikaalne(kui partofspeech on 
          print(morf_sen)
          print(partofspeech)
          for word in sen_list:
            morf_l = analyze(word)
            morf_l2 = morf_l[0]['analysis']
            if len(morf_l2) == 1:                                 #üheselt määratud sobib otsitavaks käändsõnaks
              b = morf_l2[0]
              case_info =(b['form']).split(' ')
              if len(b['root_tokens']) == 1:
                nominative = b['root_tokens'][0]
              else:
                nominative = b['root_tokens'][0]+b['root_tokens'][1]
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
                info = SubElement(content,'info')               #XML loomine
                #if sen_len <5:# and  compatibility1 == True:
                #  info.set('level','1')
                #elif compatibility2 == True:
                #  info.set('level','2')
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
                go = False
                      
    xml_formatting(content)
    tree2.write(file_name,'utf8')

#print(getBestPOSCombination(case_dict, 'proov.xml'))
#print(getBestPOSCombination(case_dict,files))
#runCaseAnalys(case_dict, 'proov.xml', 'laused.xml' )
#runCaseAnalys(case_dict, 'Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/ilu_viljakyla.tasak.xml', 'laused.xml' )
#runCaseAnalys(case_dict, 'Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/ilu_volta.tasak.xml', 'laused.xml' )















          
