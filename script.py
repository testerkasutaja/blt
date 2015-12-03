import xml.etree.ElementTree as ET
import re
from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint
import json

#syntesaatori naide
#synthesize('pood', form='pl p', partofspeech='S', phonetic=False)
# synthesize('palk', form='sg kom', phonetic=False)



tree = ET.parse('proov.xml')
root = tree.getroot()

#käänete sõnastik
case_dict = {'sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seesütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','n':'nimetav','p':'osastav','ter':'rajav','tr':'saav'}

for elem in root.findall('.//s'):
    sen=elem.text
    sen = re.sub('^ | $', '', sen)
    morf_sen = re.sub(' (,|\.|!|\?)', '', sen)
    sen_list = morf_sen.split(' ')
    if len(sen_list)>2 and len(sen_list)<11:
        #käime lause läbi
        for word in sen_list:
            morf_l = analyze(word)
            for a in morf_l:
                morf_l2 = (a['analysis'])
                for b in morf_l2:
                    case_info =(b['form']).split(' ')
                    if len(case_info)== 2 and case_info[0] in case_dict and case_info[1] in case_dict: #kui on käändsõna
                        sg_pl = case_info[0]# ainus v mitmus
                        case = case_info[1]# kääne
                        print(word)
                        print('Kääne: ', case_dict[case])
                        print('Ainus/mitmus: ', case_dict[sg_pl])
                        print()
                    else:
                        print(word, '<--pole käändsõna')
