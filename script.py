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

case_dict = {'n':'nimetav','sg':'ainsus','pl':'mitmus','ab':'ilmaütlev','abl':'alaltütlev','ad':'alalütlev','adt':'lühike sisseütlev','all':'alaleütlev','el':'seestütlev','es':'olev','g':'omastav','ill':'sisseütlev','in':'seesütlev','kom':'kaasaütlev','p':'osastav','ter':'rajav','tr':'saav'}
files  = glob.glob("Eesti_ilukirjandus/ilukirjandus/Eesti_ilukirjandus_1990/*")
inappropriateWords = ['loll', ',jama', 'kurat', 'kapo', 'kanep', 'tegelt', 'sitt', 'pätt', 'in', 'mats', 'homo', 'pagan', 'joodik', 'idioot', 'nats', 'point', 'kesik', 'aa', 'neeger', 'veits', 'jurama', 'narkomaan', 'jobu', 'siuke', 'õps', 'perse', 'tibi', 'riist', 'aint', 'tiss', 'pask', 'raisk', 'värdjas', 'prostituut', 'pedofiil', 'mupo', 'gei', 'suli', 'porno', 'kaabakas', 'pepupeldik', 'kaka', 'piss', 'tibla', 'möla', 'lollakas', 'luuser', 'lits', 'tatt', 'pissima', 'vets', 'lesbi', 'ment', 'pede', 'inf', 'eepervert', 'narkar', 'okse', 'bemm', 'penskar', 'kusema', 'kakama', 'rullnokk', 'tola', 'rulima', 'junn', 'tglt', 'ubekas', 'peer', 'out', 'pedofiilia', 'muti', 'tõbras', 'sittuma', 'kaak', 'totakas', 'pee', 'kuramus', 'debiilik', 'tutt', 'diiler', 'ila', 'kommar', 'pilu', 'raibe', 'kusifašist', 'paganama', 'keppima', 'tra', 'moll', 'tips', 'kuradima', 'pohhui', 'pederast', 'pandav', 'kommu', 'jõmm', 'vänt', 'beib', 'friik', 'nolk', 'tegelinski', 'totu', 'möga', 'oss', 'mölakas', 'lurjus', 'mõrd', 'fašistlik', 'kaif', 'noku', 'argpüks', 'tatikas', 'mate', 'ajukääbik', 'liputamavibraator', 'lollpea', 'sitane', 'memmekas', 'lõust', 'somm', 'idikas', 'bordell', 'kärvama', 'kärakas', 'kemps', 'hoor', 'iiling', 'pederastia', 'narkots', 'vant', 'hui', 'hui', 'venku', 'sitasti', 'nodi', 'soperdis', 'tõusik', 'puuks', 'äbarik', 'vitt', 'libu', 'hulkur', 'enivei', 'looderpeeretama', 'peda', 'tolgus', 'lontrus', 'pohh', 'hängima', 'sunnik', 'jätis', 'türa', 'jura', 'laiskvorst', 'drive-in', 'kiim', 'matslik', 'sittama', 'debiil', 'rops', 'mimm', 'kurivaim', 'sitapea', 'jota', 'nahhui', 'tšikk', 'veitsa', 'bitch', 'dire', 'linnavurle', 'russ', 'prost', 'empstumba', 'burks', 'shoppama', 'pabul', 'keska', 'tohman', 'peldik', 'bemar', 'kretiin', 'liputaja', 'tainapea', 'varganägu', 'litakas', 'värdjalik', 'haip', 'litsakas', 'molu', 'kaltsakas', 'vanka', 'lojus', 'kähkukas', 'sovett', 'närakas', 'töllmokk', 'prükkar', 'häbe', 'hooramakagebiit', 'tipsi', 'kantpea', 'skinhead', 'hullar', 'keelekas', 'lasteporno', 'ruts', 'nikkuma', 'chillima', 'šoppama', 'komnoor', 'lausloll', 'logard', 'tuhvlialune', 'piff', 'mata', 'matslus', 'lipakas', 'pasandama', 'ropsima', 'memmepoeg', 'tattnina', 'puuksutama', 'skisonatsistlik', 'molkus', 'pohui', 'tillu', 'pissipott', 'kusik', 'jobukakk', 'niuke', 'litsimaja', 'närukael', 'pohuism', 'haipima', 'pilusilm', 'juhmakas', 'puts', 'julk', 'vurle', 'pursui', 'blatnoi', 'komu', 'kuram', 'tuss', 'baaba', 'näss', 'hoorus', 'kakane', 'sitakott', 'lita', 'sopakaspohhuist', 'grupiseks', 'nuss', 'ponks', 'joomar', 'skinn', 'samakas', 'trulla', 'frits', 'eniveis', 'sitahunnik', 'kurask', 'jokkis', 'huinjaa', 'sitahais', 'sakuska', 'tots', 'amf', 'morda', 'nussima', 'sakumm', 'pissitama', 'sitavares', 'sitaratas', 'kili', 'jeestlane', 'gümna', 'platnoigigolo', 'mamps', 'sekspomm', 'kürb', 'tšillima', 'kaki', 'pilukas', 'ladna', 'duubeldama', 'jobukari', 'tšau', 'krõhva', 'haisukott', 'perseli', 'kehka', 'klassijuss', 'pohhuistlik', 'kabistama', 'plää', 'linnusitt', 'nahui', 'sitajunn', 'toksikomaan', 'pordumaja', 'labrakasnarkomuul', 'joobar', 'masuurikas', 'nässakas', 'kräu', 'ciao', 'lirva', 'persevest', 'koinima', 'sitaauk', 'tsillima', 'samagonntöpa', 'sopajoodik', 'tšuhnaa', 'larhv', 'ajukääbus', 'kiimlema', 'jobi', 'porduelu', 'sitahäda', 'tõprakari', 'kirvenägu', 'odratolgus', 'kakimakiimakott', 'kräkk', 'saksmann', 'bomž', 'kusev', 'plebei', 'pasahunnik', 'sakusment', 'pasakott', 'kabajantsik', 'kiimalus', 'milf', 'pano', 'litapoeg', 'jobutamapohhuilt', 'grupiks', 'topakas', 'hooramaja', 'türapea', 'küberseks', 'pepuvahe', 'kusene', 'kusija', 'hoorapoeg', 'pizdets', 'hohollpasanteeria', 'bitš', 'kekats', 'kakanoku', 'panomees', 'nadikael', 'pärakas', 'tolbajoob', 'kusetama', 'bljät', 'bizdets', 'pleiboi', 'pasahais', 'kagebist', 'praagamagu', 'bljat', 'kiimlus', 'pedetsema', 'nihhuijaa', 'nehhui', 'häbedus', 'häbemepilu', 'jobama', 'kuselema', 'kagebeelanemunapiiks', 'oolrait', 'beibe', 'jobutus', 'sigarijunn', 'sitavedaja', 'dolbajoob', 'jobisema', 'pipravitt', 'türahiinlane', 'perseklile', 'tindinikkuja']



def fixPunctuation(sentence):                             #kui lause on " lause lause lasue ? " siis eemaldatakse jutumärgid ( ” , ", “)
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

def listtostring(list):
  str = ', '.join(list)
  return str

def getPosWithMorfaA(corpus):
  posList = []
  disamb = Disambiguator()
  texts = disamb.disambiguate(corpus)
  for text in texts:
    for word in text.words:
        if len(word[ANALYSIS]) > 1:
          #print(word[TEXT],[(a[POSTAG],a[FORM], a[LEMMA]) for a in word[ANALYSIS]])
          return []
        else:
          #print(word[TEXT],[(a[POSTAG],a[FORM], a[LEMMA]) for a in word[ANALYSIS]])
          for a in word[ANALYSIS]:
            partOfSpeech = a[POSTAG]
            if partOfSpeech != 'Z':
              posList.append(partOfSpeech)
  return posList

def addToDictionary(pos_str,combinations,structure_with_sentences,sen):
  if pos_str in combinations:
    old = combinations[pos_str]
    new = old +1
    combinations[pos_str] = new
    if sen not in structure_with_sentences[pos_str]:
      structure_with_sentences[pos_str].append(sen)
  else:
    combinations[pos_str] = 1
    structure_with_sentences[pos_str] = []
    structure_with_sentences[pos_str].append(sen)
  return(combinations,structure_with_sentences)

def chooseSentencesFromCorpus(files):
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
        corpus = [sen]
        posList = getPosWithMorfaA(corpus)
        sentenceLen = len(posList)
        pos_str = listtostring(posList)
        if sentenceLen > 2 and sentenceLen < 7 and 'V' in posList:
          if sentenceLen == 3:
            (combinations3words,structure_with_sentences_3)=addToDictionary(pos_str,combinations3words,structure_with_sentences_3,sen)
          if sentenceLen == 4:
            (combinations4words,structure_with_sentences_4)=addToDictionary(pos_str,combinations4words,structure_with_sentences_4,sen)
          if sentenceLen == 5:
            (combinations5words,structure_with_sentences_5)=addToDictionary(pos_str,combinations5words,structure_with_sentences_5,sen)        

  return (combinations3words,combinations4words,combinations5words,structure_with_sentences_3,structure_with_sentences_4,structure_with_sentences_5)

def getCommonSentences(combinations,structure_with_sentences):
  sentences= []
  notCommonSen = []
  if len(combinations)>0:
    sorted_com = sorted(combinations.values())
    maximum = sorted_com[-1]
    minimum = (maximum//8)
    for k, v in combinations.items():
      if v >= minimum:
        listofsentences = structure_with_sentences.get(k)
        for sentence in listofsentences:
          sentences.append(sentence)
      else:
        listofsentences = structure_with_sentences.get(k)
        for sentence in listofsentences:
           notCommonSen.append(sentence)
  #print(notCommonSen)
  return(sentences)


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
      sentence = " " + sentence + " "
      corpus = [sentence] 
      disamb = Disambiguator()
      texts = disamb.disambiguate(corpus)
      for text in texts:
        for word in text.words:
          if appropriateSentence == True:
            for a in word[ANALYSIS]:
              if a[POSTAG] != 'Z':
                case_info = a[FORM].split(' ')
                nominative = a[LEMMA]
                thisWord = word[TEXT]
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
                    sen_x = re.sub(' ' + thisWord + ' ',' %%% ',sentence)
                    if casename != "n" or casename =="n" and sg_pl == "pl":
                      (content_all) = addToContent(thisWord, content_all, casename, id, nominative, sen_x,sg_pl)
                      id = id + 1 
                      added = True
                    if casename == "n" and sg_pl == "pl":
                      content_n = addToContent(thisWord, content_n, casename, id, nominative, sen_x, sg_pl)
                      added = True
                    if casename == "g" or casename=="es":
                      (content_g_es)= addToContent(thisWord, content_g_es, casename, id, nominative, sen_x,sg_pl)
                      added = True
                    if casename == "p":
                      (content_p)= addToContent(thisWord, content_p, casename, id, nominative, sen_x,sg_pl)
                      added = True
                    if casename == "ill" or casename == "in" or casename == "el" or casename == "adt" or casename == "all" or casename == "ad" or casename == "abl":
                      (content_ill)= addToContent(thisWord, content_ill, casename, id, nominative, sen_x,sg_pl)
                      added = True
                    if casename == "tr" or casename=="ter" or casename=="ab" or casename=="kom":
                      (content_tr_ter_ab_kom) = addToContent(thisWord, content_tr_ter_ab_kom, casename, id, nominative, sen_x,sg_pl)
                      added = True                
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

                  
  else:
    print('Laused analüüsimiseks puuduvad')


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





(combin3,combin4,combin5,sentences_with_structure_3, sentences_with_structure_4, sentences_with_structure_5) = chooseSentencesFromCorpus(files)

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




            
