import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement

import re
from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint


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

#käänete sõnastik
case_dict = {'sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seesütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}



def structureCompatibility(list):
  structure = [['V',['S',['D',['J',['V',['S']]]]]],['S',['V',['D',['J',['V',['S']]]]]]]
  for i in range(len(list)):
   for elem in structure:
     for a in elem:
       print(a)#esimene
    
  
l=['V',['S',['D',['J',['V',['S']]]]]]

structureCompatibility(l)




def runCaseAnalys(case_dict, pathStr ):
    go = False
    tree = ET.parse(pathStr)
    root = tree.getroot()
    count=0
    content = ET.Element('content')
    tree2 = ElementTree(content)
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
        sen = elem.text
        sen = re.sub('^ | $', '', sen)
        morf_sen = re.sub(' (,|\.|!|\?)', '', sen)
        sen_list = morf_sen.split(' ')
        partOfSpeech = []
        if len(sen_list)>2 and len(sen_list)<11:                        #käime lause läbi
            for word in sen_list:
              morf_l = analyze(word)
              for a in morf_l:#morfi esimene
                morf_l2 = (a['analysis'])
                
                for b in morf_l2:
                  #print(word)
                  #print(b['partofspeech'])
                  partOfSpeech.append([b['partofspeech']])
                  if len(morf_l2) == 1:           #üheselt määratud sobib otsitavaks sõnaks
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
                        info = SubElement(content,'info')              #XML loomine
                        info.set('id', str(count))
                        count = count + 1
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
                  
        #print(partOfSpeech)                                         
        #print(len(partOfSpeech))                      

                                
    #print(partOfSpeech)                       
    xml_formatting(content)
    tree2.write('laused.xml','utf8')


runCaseAnalys(case_dict, 'proov.xml')
#runCaseAnalys(case_dict, 'Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/ilu_viljakyla.tasak.xml')








