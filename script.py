import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

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


tree = ET.parse('proov.xml')
root = tree.getroot()

content = Element('content')
tree2 = ElementTree(content)


#käänete sõnastik
case_dict = {'sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seesütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}

for elem in root.findall('.//s'):
    sen = elem.text
    sen = re.sub('^ | $', '', sen)
    morf_sen = re.sub(' (,|\.|!|\?)', '', sen)
    sen_list = morf_sen.split(' ')
    more = 0
    if len(sen_list)>2 and len(sen_list)<13:
                                                           #käime lause läbi
        for word in sen_list:
            morf_l = analyze(word)
            for a in morf_l:                                #morfi esimene list
                morf_l2 = (a['analysis'])
                if len(morf_l2) == 1:                          #kui mitu dict'i sees siis esialgu ei sobi
                    for b in morf_l2:                       #teine morfi list
                        case_info =(b['form']).split(' ')
                        nominative = b['root_tokens'][0]
                        if len(case_info)== 2 and case_info[0] in case_dict and case_info[1] in case_dict: #kui on käändsõna
                            sg_pl = case_info[0]                # ainus v mitmus
                            casename = case_info[1]                 # kääne         
                            sen_x = re.sub(word,'%%%',sen)

                            info = Element('info')              #XML loomine
                            content.append(info)
                            s = ET.SubElement(info,'s')
                            answer = Element('answer')
                            info.append(answer)
                            nr = Element('nr')
                            info.append(nr)
                            case = Element('case')
                            info.append(case)
                            n = Element('n')
                            info.append(n)


                            nr.text = case_dict[sg_pl]  
                            n.text = nominative
                            case.text = case_dict[casename]
                            answer.text = word
                            s.text = sen_x
xml_formatting(content)
tree2.write('laused.xml','utf8')








