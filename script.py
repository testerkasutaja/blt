import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import glob
import re
import operator
import estnltk
from pprint import pprint
from estnltk.names import TEXT, ANALYSIS, ROOT, POSTAG, FORM, LEMMA, CLITIC, ROOT_TOKENS
from estnltk import Disambiguator
from estnltk import synthesize
from estnltk import Text
from estnltk import teicorpus
import time

case_dict = {'n':'nimetav','sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seestütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")
inappropriateWords = ['loll', ',jama', 'kurat', 'kapo', 'kanep', 'tegelt', 'sitt', 'pätt', 'in', 'mats', 'homo', 'pagan', 'joodik', 'idioot', 'nats', 'point', 'kesik', 'aa', 'neeger', 'veits', 'jurama', 'narkomaan', 'jobu', 'siuke', 'õps', 'perse', 'tibi', 'riist', 'aint', 'tiss', 'pask', 'raisk', 'värdjas', 'prostituut', 'pedofiil', 'mupo', 'gei', 'suli', 'porno', 'kaabakas', 'pepupeldik', 'kaka', 'piss', 'tibla', 'möla', 'lollakas', 'luuser', 'lits', 'tatt', 'pissima', 'vets', 'lesbi', 'ment', 'pede', 'inf', 'eepervert', 'narkar', 'okse', 'bemm', 'penskar', 'kusema', 'kakama', 'rullnokk', 'tola', 'rulima', 'junn', 'tglt', 'ubekas', 'peer', 'out', 'pedofiilia', 'muti', 'tõbras', 'sittuma', 'kaak', 'totakas', 'pee', 'kuramus', 'debiilik', 'tutt', 'diiler', 'ila', 'kommar', 'pilu', 'raibe', 'kusifašist', 'paganama', 'keppima', 'tra', 'moll', 'tips', 'kuradima', 'pohhui', 'pederast', 'pandav', 'kommu', 'jõmm', 'vänt', 'beib', 'friik', 'nolk', 'tegelinski', 'totu', 'möga', 'oss', 'mölakas', 'lurjus', 'mõrd', 'fašistlik', 'kaif', 'noku', 'argpüks', 'tatikas', 'mate', 'ajukääbik', 'liputamavibraator', 'lollpea', 'sitane', 'memmekas', 'lõust', 'somm', 'idikas', 'bordell', 'kärvama', 'kärakas', 'kemps', 'hoor', 'iiling', 'pederastia', 'narkots', 'vant', 'hui', 'hui', 'venku', 'sitasti', 'nodi', 'soperdis', 'tõusik', 'puuks', 'äbarik', 'vitt', 'libu', 'hulkur', 'enivei', 'looderpeeretama', 'peda', 'tolgus', 'lontrus', 'pohh', 'hängima', 'sunnik', 'jätis', 'türa', 'jura', 'laiskvorst', 'drive-in', 'kiim', 'matslik', 'sittama', 'debiil', 'rops', 'mimm', 'kurivaim', 'sitapea', 'jota', 'nahhui', 'tšikk', 'veitsa', 'bitch', 'dire', 'linnavurle', 'russ', 'prost', 'empstumba', 'burks', 'shoppama', 'pabul', 'keska', 'tohman', 'peldik', 'bemar', 'kretiin', 'liputaja', 'tainapea', 'varganägu', 'litakas', 'värdjalik', 'haip', 'litsakas', 'molu', 'kaltsakas', 'vanka', 'lojus', 'kähkukas', 'sovett', 'närakas', 'töllmokk', 'prükkar', 'häbe', 'hooramakagebiit', 'tipsi', 'kantpea', 'skinhead', 'hullar', 'keelekas', 'lasteporno', 'ruts', 'nikkuma', 'chillima', 'šoppama', 'komnoor', 'lausloll', 'logard', 'tuhvlialune', 'piff', 'mata', 'matslus', 'lipakas', 'pasandama', 'ropsima', 'memmepoeg', 'tattnina', 'puuksutama', 'skisonatsistlik', 'molkus', 'pohui', 'tillu', 'pissipott', 'kusik', 'jobukakk', 'niuke', 'litsimaja', 'närukael', 'pohuism', 'haipima', 'pilusilm', 'juhmakas', 'puts', 'julk', 'vurle', 'pursui', 'blatnoi', 'komu', 'kuram', 'tuss', 'baaba', 'näss', 'hoorus', 'kakane', 'sitakott', 'lita', 'sopakaspohhuist', 'grupiseks', 'nuss', 'ponks', 'joomar', 'skinn', 'samakas', 'trulla', 'frits', 'eniveis', 'sitahunnik', 'kurask', 'jokkis', 'huinjaa', 'sitahais', 'sakuska', 'tots', 'amf', 'morda', 'nussima', 'sakumm', 'pissitama', 'sitavares', 'sitaratas', 'kili', 'jeestlane', 'gümna', 'platnoigigolo', 'mamps', 'sekspomm', 'kürb', 'tšillima', 'kaki', 'pilukas', 'ladna', 'duubeldama', 'jobukari', 'tšau', 'krõhva', 'haisukott', 'perseli', 'kehka', 'klassijuss', 'pohhuistlik', 'kabistama', 'plää', 'linnusitt', 'nahui', 'sitajunn', 'toksikomaan', 'pordumaja', 'labrakasnarkomuul', 'joobar', 'masuurikas', 'nässakas', 'kräu', 'ciao', 'lirva', 'persevest', 'koinima', 'sitaauk', 'tsillima', 'samagonntöpa', 'sopajoodik', 'tšuhnaa', 'larhv', 'ajukääbus', 'kiimlema', 'jobi', 'porduelu', 'sitahäda', 'tõprakari', 'kirvenägu', 'odratolgus', 'kakimakiimakott', 'kräkk', 'saksmann', 'bomž', 'kusev', 'plebei', 'pasahunnik', 'sakusment', 'pasakott', 'kabajantsik', 'kiimalus', 'milf', 'pano', 'litapoeg', 'jobutamapohhuilt', 'grupiks', 'topakas', 'hooramaja', 'türapea', 'küberseks', 'pepuvahe', 'kusene', 'kusija', 'hoorapoeg', 'pizdets', 'hohollpasanteeria', 'bitš', 'kekats', 'kakanoku', 'panomees', 'nadikael', 'pärakas', 'tolbajoob', 'kusetama', 'bljät', 'bizdets', 'pleiboi', 'pasahais', 'kagebist', 'praagamagu', 'bljat', 'kiimlus', 'pedetsema', 'nihhuijaa', 'nehhui', 'häbedus', 'häbemepilu', 'jobama', 'kuselema', 'kagebeelanemunapiiks', 'oolrait', 'beibe', 'jobutus', 'sigarijunn', 'sitavedaja', 'dolbajoob', 'jobisema', 'pipravitt', 'türahiinlane', 'perseklile', 'tindinikkuja']


def makeFreqDictToList(inappropriateWords):
  freqWordList = []
  with open('FreqDictionary/lemmas_utf8.txt','r',encoding='utf8') as f:
    content = f.readlines()[1:]
    for elem in content:
      elem = elem.split('\t')
      word = elem[0]
      if word not in inappropriateWords:
        #print(word)
        freqWordList.append(word)
      
  return freqWordList


def fixPunctuation(sentence):                             #kui lause on " lause lause lasue ? " siis eemaldatakse jutumärgid ( ” , ", “)
  sentence = re.sub('^\s|\s$', '', sentence)
  sentence = re.sub('”', '"', sentence)
  sentence = re.sub('“', '"', sentence)
  if sentence.count('"')== 1 or sentence.count('"')== 3 or sentence.count('"') > 4 or ":" in sentence or "(" in sentence or ")" in sentence :
    sentence = ""
    return sentence
  if sentence.count('%%%')== 1:
    print(sentence)
  if sentence.count('"')== 2 and sentence.endswith('"') and sentence.startswith('"'):
    sentence = re.sub('^"|"$', '', sentence)
  sentence = re.sub('^\s|\s$', '', sentence)
  return sentence

def listtostring(list):
  str = ', '.join(list)
  return str


def addToDictionary(pos_str,combinations,structure_with_sentences,sen_info):
  if pos_str in combinations:
    old = combinations[pos_str]
    new = old +1
    combinations[pos_str] = new
    if sen_info not in structure_with_sentences[pos_str]:
      structure_with_sentences[pos_str].append(sen_info)

  else:
    combinations[pos_str] = 1
    structure_with_sentences[pos_str] = []
    structure_with_sentences[pos_str].append(sen_info)
  return(combinations,structure_with_sentences)

def chooseSentencesFromCorpus(files,freqWordList,inappropriateWords):
  combinations3words = {}
  combinations4words = {}
  combinations5words = {}
  combinations6words = {}
  combinations7words = {}
  structure_with_sentences_3 = {}
  structure_with_sentences_4 = {}
  structure_with_sentences_5 = {}
  structure_with_sentences_6 = {}
  structure_with_sentences_7 = {}
  for pathStr in files:
    print(pathStr)
    tree = ET.parse(pathStr)
    root = tree.getroot()
    corpus = []
    for title in root.findall('.//{http://www.tei-c.org/ns/1.0}title'):
      title = title.text
    for elem in root.findall('.//{http://www.tei-c.org/ns/1.0}s'):
      sentence = elem.text
      sentence = fixPunctuation(sentence)
      if sentence.endswith('"') or sentence.endswith('.') or sentence.endswith('!') or sentence.endswith('?') and sentence != "":
        corpus.append(sentence)
    disamb = Disambiguator()
    texts = disamb.disambiguate(corpus)
    for text in texts:
      valid = True
      clitics=[]
      ambDict = text.get.postags.as_dict
      posList = ambDict.get('postags')
      while posList.count('Z') > 0:
        posList.remove('Z')
      sentenceLen=len(posList)
      pos_str = listtostring(posList)
      if sentenceLen > 2 and sentenceLen < 8 and 'V' in posList:
        for word in text.words:       #Kui sõnal on rohkem kui 1 analüüs, siis lausei ei sobi, sest lause pole üheselt määratud
          if len(word[ANALYSIS]) > 1:
            valid = False
          else:
            for a in word[ANALYSIS]:
              pos = a[POSTAG]
              lemma = a[LEMMA]
              if pos != 'Z':
                if lemma not in freqWordList:  #Kontroll kas sõna kuulub sagedussõnastikku
                  #print('Lemam ei ole freq: ',text)
                  #print(lemma)
                  
                  valid = False
              if valid == True:
                clitic = a[CLITIC]
                clitics.append(clitic)
        if valid == True:             #Lauses pole sõna millel on rohkem kui üks analüüs ning pole sõna mille liitsõna või sõna kuulub ebasobivate lausete hulka
          sentence_analysis = text.get.word_texts.lemmas.forms.as_dict
          root_tokens =text.get.root_tokens.as_dict
          sentence_analysis['clitics'] = clitics
          sentence_analysis['title'] = title
          if sentenceLen == 3:
            (combinations3words,structure_with_sentences_3)=addToDictionary(pos_str,combinations3words,structure_with_sentences_3,sentence_analysis)
          if sentenceLen == 4:
            (combinations4words,structure_with_sentences_4)=addToDictionary(pos_str,combinations4words,structure_with_sentences_4,sentence_analysis)
          if sentenceLen == 5:
            (combinations5words,structure_with_sentences_5)=addToDictionary(pos_str,combinations5words,structure_with_sentences_5,sentence_analysis)
          if sentenceLen == 6:
              (combinations6words,structure_with_sentences_6)=addToDictionary(pos_str,combinations6words,structure_with_sentences_6,sentence_analysis)
          if sentenceLen == 7:
              (combinations7words,structure_with_sentences_7)=addToDictionary(pos_str,combinations7words,structure_with_sentences_7,sentence_analysis)

  return (combinations3words,combinations4words,combinations5words,combinations6words,combinations7words,structure_with_sentences_3,structure_with_sentences_4,structure_with_sentences_5,structure_with_sentences_6,structure_with_sentences_7)

def getCommonSentences(combinations,structure_with_sentences):
  sentences= []
  if len(combinations)>0:
    sorted_com = sorted(combinations.values())
    maximum = sorted_com[-1]
    minimum = (maximum//2.5)
    for k, v in combinations.items():
      if v >= minimum:
        listofsentences = structure_with_sentences.get(k)
        for sentence in listofsentences:
          sentences.append(sentence)
  return(sentences)


def formatXMLFile(elem, level=0):  # internetist saadud funktsioon. Lehelt: http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
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

def getSentence(sen_list):
  sentence = " "
  for word in sen_list:
    sentence = sentence + word + " "
  return sentence
    

def runCaseAnalys(case_dict, list_of_sentences,inappropriateWords):
  print('case analys start')
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
    for sentence_info in list_of_sentences:
      forms = sentence_info.get('forms')
      lemmas = sentence_info.get('lemmas')
      sentence_as_list = sentence_info.get('word_texts')
      title = sentence_info.get('title')
      sentence = getSentence(sentence_as_list)
      named_entities = sentence_info.get('named_entities')
      clitics = sentence_info.get('clitics')
      roots = sentence_info.get('root_tokens')
      for index in range(len(forms)):
          form = forms[index]
          if form != '':
            nominative = lemmas[index]
            word =sentence_as_list[index]
            clitic = clitics[index]
            case_info = form.split(' ')
            if case_info[0]=='adt':                           #Lühikesisseütlev
              casename = case_info[0]
              sg_pl='sg'
              go = True
            elif (len(case_info)== 2) and (case_info[0] in case_dict) and (case_info[1] in case_dict): #kui on käändsõna
              sg_pl = case_info[0]                            # ainus v mitmus   
              casename = case_info[1]                         # kääne
              go = True
            if go == True:
              sen_x = re.sub(' ' + word + ' ',' %%% ',sentence)
              if casename != "n" or casename =="n" and sg_pl == "pl":
                content_all = addToContent(word, content_all, casename, id, nominative, sen_x,sg_pl,title,clitic)
              if casename == "n" and sg_pl == "pl":
                content_n = addToContent(word, content_n, casename, id, nominative, sen_x, sg_pl,title,clitic)    
              if casename == "g" or casename=="es":
                 content_g_es = addToContent(word, content_g_es, casename, id, nominative, sen_x,sg_pl,title,clitic)
              if casename == "p":
                content_p= addToContent(word, content_p, casename, id, nominative, sen_x,sg_pl,title,clitic)     
              if casename == "ill" or casename == "in" or casename == "el" or casename == "adt" or casename == "all" or casename == "ad" or casename == "abl":
                content_ill = addToContent(word, content_ill, casename, id, nominative, sen_x,sg_pl,title,clitic)      
              if casename == "tr" or casename=="ter" or casename=="ab" or casename=="kom":
                content_tr_ter_ab_kom = addToContent(word, content_tr_ter_ab_kom, casename, id, nominative, sen_x,sg_pl,title,clitic)
      id = id + 1
      go = False

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
  else:
    print('Laused analüüsimiseks puuduvad.')

def addToContent(word, content, casename, countid, nominative, sen_x,sg_pl,title,clitic):
              info = SubElement(content,'info')             #XML loomine
              info.set('id', str(countid))
              s = SubElement(info,'s')
              nr = SubElement(info,'nr')
              case = SubElement(info,'case')
              n = SubElement(info,'n')
              synt = synthesize(nominative, form = sg_pl+' '+casename, hint = word)      #kontorll kas leidub rohkem kui üks vastus
              if len(synt)>1:
                wordLower = word.lower()
                if wordLower in synt:  
                  for nom in synt:
                    if nom != wordLower:
                      answer = SubElement(info, 'answer')
                      answer.text= nom 
              answer = SubElement(info, 'word')
              answer.text = word
              n.text = nominative
              nr.text = case_dict[sg_pl]  
              case.text = case_dict[casename]
              s.text = sen_x
              if clitic != "":
                cliticTag = SubElement(info,'clitic')
                cliticTag.text = clitic
              titleTag = SubElement(info,'title')
              titleTag.text = title
              return content

def main():
  print (time.asctime( time.localtime(time.time()) ))
  freqWordList = makeFreqDictToList(inappropriateWords)
  print(len(freqWordList))
  (combin3,combin4,combin5,combin6,combin7,sentences_with_structure_3, sentences_with_structure_4, sentences_with_structure_5, sentences_with_structure_6,sentences_with_structure_7) = chooseSentencesFromCorpus(files,freqWordList,inappropriateWords)
  three_word_sentences = getCommonSentences(combin3,sentences_with_structure_3)
  four_word_sentences = getCommonSentences(combin4,sentences_with_structure_4)
  five_word_sentences = getCommonSentences(combin5,sentences_with_structure_5)
  six_word_sentences = getCommonSentences(combin6,sentences_with_structure_6)
  seven_word_sentences = getCommonSentences(combin7,sentences_with_structure_7)
  print('Kolmesõnalisi lauseid on kokku: ' , (len(three_word_sentences)))
  print('Neljasõnalisi lauseid on kokku: ' , (len(four_word_sentences)))
  print('Viiesõnalisi lauseid on kokku: ' , (len(five_word_sentences)))
  print('Kuuesõnalisi lauseid on kokku: ' , (len(six_word_sentences)))
  print('Seitsmesõnalisi lauseid on kokku: ' , (len(seven_word_sentences)))
  all_sentences_info = three_word_sentences + four_word_sentences + five_word_sentences + six_word_sentences + seven_word_sentences
  runCaseAnalys(case_dict, all_sentences_info, inappropriateWords)
  print (time.asctime( time.localtime(time.time()) ))


main()




            
